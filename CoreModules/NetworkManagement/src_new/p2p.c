#include <arpa/inet.h>
#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdarg.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>

#include "./headers/p2p.h"
#include "./headers/utils.h"
#include "./headers/mq.h"
#include "./headers/router.h"

static packet snd_buffer = {};
static packet rcv_buffer = {};

char buffer[MAX_SIZE];

int get_save_size(){
    struct stat st;
    stat("../../../Assets/games/to-send.pkl", &st);
    return st.st_size;
}

void send_pickle_file(int first_conn)
{
    bzero(buffer, MAX_SIZE);
    int file_fd, bytes_read, bytes_sent;
    printf("%d\n", first_conn);
    // Ouvrir le fichier en lecture seule
    file_fd = open("../../../Assets/games/to-send.pkl", O_RDONLY);
    if (file_fd == -1)
    {
        perror("Impossible d'ouvrir le fichier");
        return;
    }

    // Lire le contenu du fichier par blocs de BUFSIZ octets et l'envoyer sur la socket
    while ((bytes_read = read(file_fd, buffer, MAX_SIZE)) > 0)
    {
        bytes_sent = send(first_conn, buffer, bytes_read, 0);
        if (bytes_sent == -1)
        {
            perror("Erreur d'envoi de données sur la socket");
            break;
        }
    }

    // Fermer le fichier et la socket
    close(file_fd);
}

void receive_picle_file(char *buffer,int n)
// le contenu reçu est directement écris dans le fichier save.pkl dans Assets/game
{
    printf("%ld\n",strlen(buffer));
    FILE *file = fopen("../../../Assets/games/to-send.pkl", "wb"); // ouvrir le fichier en mode binaire
    if (file != NULL)
    {
        fwrite(buffer, sizeof(char), n, file); // écrire le contenu du buffer dans le fichier
        fclose(file);                                       // fermer le fichier
    }
    else
    {
        printf("Impossible d'ouvrir le fichier\n");
    }
}

//SANS SERVER
void p2p_run(char *personal_address, int personal_port)
{
    printf("\033[1;33m[Setting up personal socket ...]\033[1;0m\n");
    
    // Creation du socket de reception
    printf("Personal socket : \n");
    int personal_socket_descriptor = socket(AF_INET, SOCK_STREAM, 0);
    if (personal_socket_descriptor <= 0)
    {
        stop("Socket failed");
    }
    
    // Options du sockets
    struct linger lingeropt;
    lingeropt.l_onoff = 1;
    lingeropt.l_linger = 0;  
    setsockopt(personal_socket_descriptor, SOL_SOCKET, SO_LINGER, &lingeropt, sizeof(lingeropt));
    
    printf("\tSocket descriptor : %d\n", personal_socket_descriptor);

    // Configuration du sockaddr
    struct sockaddr_in personal_sock_addr =
        {
            .sin_family = AF_INET,
            .sin_port = htons(personal_port),
            .sin_addr.s_addr = inet_addr(personal_address),
        };

    printf("Binding with :\n");
    printf("\taddress : %s\n", inet_ntoa(personal_sock_addr.sin_addr));
    printf("\tport:%d\n", ntohs(personal_sock_addr.sin_port));

    int sock_addr_size = sizeof(personal_sock_addr);

    if (bind(personal_socket_descriptor, (struct sockaddr *)&personal_sock_addr, sock_addr_size) < 0)
    {
        stop("Bind failed");
    }
    if (listen(personal_socket_descriptor, 3) < 0)
    {
        stop("Listen failed");
    }
    printf("\033[1;32m[Personal socket ok]\033[1;0m\n");

    printf("\033[1;33m[Adding current player to player list]\033[1;0m\n");

    Player self = {
        personal_sock_addr.sin_addr.s_addr,
        ntohs(personal_sock_addr.sin_port),
        personal_socket_descriptor,
    };

    router_insertElement(self);
    router_set_self(self);
    router_showList();

    printf("\033[1;32m[Current player successfully added to player list]\033[1;0m\n");

    // Préparation des sets pour le select
    fd_set totalFds;
    FD_ZERO(&totalFds);
    FD_SET(personal_socket_descriptor, &totalFds);

    // Création de 2 processus pour l'envoie et la reception des packets
    int process_id = fork();

    if (process_id == 0)
    {
        while (1)
        {
            p2p_handle_rcv(personal_socket_descriptor, (struct sockaddr *)&personal_sock_addr, sock_addr_size, &totalFds);
        }
    }
    else
    {
        while (1)
        {
            p2p_handle_snd();
        }
    }
}

void p2p_handle_rcv(int socket_descriptor, struct sockaddr *sock_addr, int sock_addr_size,fd_set *totalFds)
{
    // Préparation du set internbe au select
    fd_set readfds;
    FD_ZERO(&readfds);

    for (size_t i = 0; i < FD_SETSIZE; i++)
    {
        if (FD_ISSET(i, totalFds))
        {
            FD_SET(i, &readfds);
            printf("%ld ", i);
        }
    }
    printf("\n");

    // Select
    printf("Selecting ...\n");
    if (select(FD_SETSIZE, &readfds, NULL, NULL, NULL) < 0)
    {
        stop("Select failed");
    }
    
    for (size_t i = 0; i < FD_SETSIZE; i++)
    {
        if (!FD_ISSET(i, &readfds))
        { 
            continue;
        }
        if (i == socket_descriptor)
        {
            printf("acceptation d'un client\n");
            int new_client_socket_descriptor = accept(socket_descriptor, sock_addr, (socklen_t *)&sock_addr_size);
            FD_SET(new_client_socket_descriptor, &readfds);
            FD_SET(new_client_socket_descriptor, totalFds);
            printf("client accepté\n");
        }
        else
        {
            printf("reception d'un packet\n");
            memset(&rcv_buffer, 0, sizeof(packet));
            bzero(buffer, MAX_SIZE);
            if (recv(i, buffer, MAX_SIZE, 0) < 0)
                stop("Recv failed");
            memcpy(&rcv_buffer, buffer, sizeof(packet));
            printf("packet reçu: %d\n", rcv_buffer.type);

            if (rcv_buffer.type != 8)
            {
                printf("packet normal\n");
            }
            else
            {
                int n;
                printf("save\n");
                int taille = atoi(rcv_buffer.body);
                // sauvegarde recu-> ecrire le binaire dans un fichier et envoyer un paquet de type 8 au python pour q'uil charge ce fichier
                bzero(buffer, MAX_SIZE);
                if ((n = recv(i, buffer, taille, MSG_WAITALL)) < 0){
                    stop("Recv failed");
                }
                printf("%d bytes recu\n",n);
                receive_picle_file(buffer,n);
                rcv_buffer.type = 8;
            }
            mq_to_py(&rcv_buffer);
        }
    }
}

void p2p_handle_snd()
{
    printf("=====================================\n");
    printf("envoi d'un packet\n");
    memset(&snd_buffer, 0, sizeof(packet));
    printf("recupération d'un packet depuis le python\n");
    mq_from_py(&snd_buffer);
    printf("packet récupéré: %d\n",snd_buffer.type);
    if (snd_buffer.type == 8)
    {   
        char *minibuf = (char *)malloc(10);
        sprintf(minibuf,"%d",get_save_size());
        memset(snd_buffer.body, 0, sizeof(snd_buffer.body));
        strncpy(snd_buffer.body,minibuf,strlen(minibuf));
        router_send(snd_buffer);
        send_pickle_file(router_get_socket_by_address(snd_buffer.destination_address, snd_buffer.port));
    }
    else
    {
        if (snd_buffer.type == INIT || snd_buffer.type == SEND_IP)
        {
            int new_socket = p2p_connect_to_other_player(snd_buffer.destination_address, snd_buffer.port);
            Player new_player = {
                snd_buffer.destination_address,
                snd_buffer.port,
                new_socket,
            };

            router_insertElement(new_player);
            router_showList();
        }

        // 4294967295 == "255.255.255.255"
        if (snd_buffer.destination_address == 4294967295)
        {
            router_broadcast(snd_buffer);
        }
        else
        {
            router_send(snd_buffer);
        }
    }
}

int p2p_connect_to_other_player(int address, unsigned short port)
{
    printf("\033[1;33m[Setting new player socket ...]\033[1;0m\n");
    // Creation du socket de reception
    printf("New player socket : \n");
    int new_player_socket_descriptor = socket(AF_INET, SOCK_STREAM, 0);

    if (new_player_socket_descriptor <= 0)
        stop("Socket failed");

    printf("\tSocket descriptor : %d\n", new_player_socket_descriptor);

    // So_linger
    struct linger so_linger;
    so_linger.l_onoff = 1;
    so_linger.l_linger = 0;
    int options = 1;
    int z = setsockopt(new_player_socket_descriptor, SOL_SOCKET, SO_LINGER,
                       &so_linger, sizeof(so_linger));
    int y = setsockopt(new_player_socket_descriptor, SOL_SOCKET, SO_REUSEADDR,
                       &options, sizeof(options));
    if (z == -1 || y == -1)
    {
        stop("setsockopt so_linger");
    }

    struct sockaddr_in new_player_sock_addr =
        {
            .sin_family = AF_INET,
            .sin_port = htons(port),
            .sin_addr.s_addr = address,
        };

    if (connect(new_player_socket_descriptor, (struct sockaddr *)&new_player_sock_addr, sizeof(new_player_sock_addr)) < 0)
        stop("Connect failed");

    printf("\033[1;32m[New player socket ok]\033[1;0m\n");

    return new_player_socket_descriptor;
}
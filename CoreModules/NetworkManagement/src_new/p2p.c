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

void p2p_run_junior(char *personal_address, int personal_port, char *client2_address, int client2_port){
    printf("\033[1;33m[Setting up personal socket ...]\033[1;0m\n");
    // Creation du socket de reception
    printf("Personal socket : \n");
    struct linger lingeropt;
    lingeropt.l_onoff = 1;
    lingeropt.l_linger = 0;
    int personal_socket_descriptor = socket(AF_INET, SOCK_STREAM, 0);
    setsockopt(personal_socket_descriptor, SOL_SOCKET, SO_LINGER, &lingeropt, sizeof(lingeropt));

    if (personal_socket_descriptor <= 0)
        stop("Socket failed");

    printf("\tSocket descriptor : %d\n", personal_socket_descriptor);

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
        stop("Bind failed");

    if (listen(personal_socket_descriptor, 3) < 0)
        stop("Listen failed");

    printf("\033[1;32m[Personal socket ok]\033[1;0m\n");

    // Creation du socket d'envoie
    // ==================================================
    // | Dans le futur il faudra                        |
    // |    - Déplacer cette étape vers l'acceptation   |
    // |      de nouveaux clients                       |
    // |    - Placer le socket_descriptor dans une      |
    // |      liste chainé                              |
    // |    - Gérer le routage des packet               |
    // ==================================================
    printf("Press ENTER key to Continue\n");
    getchar();
    

    int first_player = TRUE;
    
    // MJOIN A GAME
    if (client2_address != NULL && client2_port!= 0){
        first_player = FALSE;
        printf("\033[1;33m[Setting up client2 socket ...]\033[1;0m\n");
        int client2_socket_descriptor = socket(AF_INET, SOCK_STREAM, 0);
        setsockopt(client2_socket_descriptor, SOL_SOCKET, SO_LINGER, &lingeropt, sizeof(lingeropt));

        if (client2_socket_descriptor < 0)
            stop("Socket Failed");

        struct sockaddr_in client2_sock_addr =
            {
                .sin_family = AF_INET,
                .sin_port = htons(client2_port),
                .sin_addr.s_addr = inet_addr(client2_address),
            };

        if (connect(client2_socket_descriptor, (struct sockaddr *)&client2_sock_addr, sizeof(client2_sock_addr)) < 0)
            stop("Connect failed");

        printf("\033[1;32m[client2 socket ok]\033[1;0m\n");
    }

    // Création de 2 processus pour l'envoie et la reception des packets
    int process_id = fork();
    if (process_id == 0){
        int client_socket_descriptor = -1;
        while (1)
            p2p_handle_rcv(personal_socket_descriptor, (struct sockaddr *)&personal_sock_addr, sock_addr_size, &client_socket_descriptor);
    }
    else{
        // Waiting for multiclient connection managment
        while (1){
            //p2p_handle_snd(client2_socket_descriptor);
            printf("Pas géré pour le moment \n");
        }
            
    }

}


void p2p_run(char *personal_address, int personal_port, char *client2_address, int client2_port)
{
    printf("\033[1;33m[Setting up personal socket ...]\033[1;0m\n");
    // Creation du socket de reception
    printf("Personal socket : \n");
    struct linger lingeropt;
    lingeropt.l_onoff = 1;
    lingeropt.l_linger = 0;
    int personal_socket_descriptor = socket(AF_INET, SOCK_STREAM, 0);
    setsockopt(personal_socket_descriptor, SOL_SOCKET, SO_LINGER, &lingeropt, sizeof(lingeropt));

    if (personal_socket_descriptor <= 0)
        stop("Socket failed");

    printf("\tSocket descriptor : %d\n", personal_socket_descriptor);

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
        stop("Bind failed");

    if (listen(personal_socket_descriptor, 3) < 0)
        stop("Listen failed");

    printf("\033[1;32m[Personal socket ok]\033[1;0m\n");

    // Creation du socket d'envoie
    // ==================================================
    // | Dans le futur il faudras                       |
    // |    - Déplacer cette étape vers l'acceptation   |
    // |      de nouveaux clients                       |
    // |    - Placer le socket_descriptor dans une      |
    // |      liste chainé                              |
    // |    - Gérer le routage des packet               |
    // ==================================================
    printf("Press ENTER key to Continue\n");
    getchar();

    printf("\033[1;33m[Setting up client2 socket ...]\033[1;0m\n");
    int client2_socket_descriptor = socket(AF_INET, SOCK_STREAM, 0);
    setsockopt(client2_socket_descriptor, SOL_SOCKET, SO_LINGER, &lingeropt, sizeof(lingeropt));
    
    if (client2_socket_descriptor < 0)
        stop("Socket Failed");

    struct sockaddr_in client2_sock_addr =
        {
            .sin_family = AF_INET,
            .sin_port = htons(client2_port),
            .sin_addr.s_addr = inet_addr(client2_address),
        };

    
    if (connect(client2_socket_descriptor, (struct sockaddr *)&client2_sock_addr, sizeof(client2_sock_addr)) < 0)
        stop("Connect failed");

    printf("\033[1;32m[client2 socket ok]\033[1;0m\n");

    // Création de 2 processus pour l'envoie et la reception des packets
    int client_socket_descriptor = -1;
    int process_id = fork();
    if (process_id == 0){
        while (1)
            p2p_handle_rcv(personal_socket_descriptor, (struct sockaddr *)&personal_sock_addr, sock_addr_size,&client_socket_descriptor);
    }
    else
        while (1)
            p2p_handle_snd(client2_socket_descriptor, &client_socket_descriptor);
}

void p2p_handle_rcv(int socket_descriptor, struct sockaddr *sock_addr, int sock_addr_size,int *client_socket_descriptor)
{
    fd_set readfds;
    FD_ZERO(&readfds);
    FD_SET(socket_descriptor, &readfds);
    if (*client_socket_descriptor != -1){
        printf("client socket descriptor : %d\n",*client_socket_descriptor);
        FD_SET(*client_socket_descriptor, &readfds);
    }
    printf("Selecting ...\n");
    if (select(FD_SETSIZE, &readfds, NULL, NULL, NULL) < 0)
        stop("Select failed");
    printf("Select ok\n");
    for (size_t i = 0; i < FD_SETSIZE; i++)
    {
        if (!FD_ISSET(i, &readfds))
            continue;

        if (i == socket_descriptor)
        {
            printf("acceptation d'un client\n");
            int new_client_socket_descriptor = accept(socket_descriptor, sock_addr, (socklen_t *)&sock_addr_size);
            FD_SET(new_client_socket_descriptor, &readfds);
            *client_socket_descriptor = new_client_socket_descriptor;
        }
        else
        {
            printf("reception d'un packet\n");
            memset(&rcv_buffer, 0, sizeof(packet));
            bzero(buffer, MAX_SIZE);
            int n;
            if ((n = recv(i, buffer, MAX_SIZE, 0)) < 0)
                stop("Recv failed");
            memcpy(&rcv_buffer, buffer, sizeof(packet));
            printf("packet reçu\n");
            if (rcv_buffer.type != 8)
            {
                printf("packet normal\n");
                mq_to_py(&rcv_buffer);
            }
            else
            {
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
                mq_to_py(&rcv_buffer);
            }
        }
    }
}

void p2p_handle_snd(int client2_socket_descriptor, int *client_socket_descriptor)
{
    printf("=====================================\n");
    printf("envoi d'un packet\n");
    memset(&snd_buffer, 0, sizeof(packet));
    printf("recupération d'un packet depuis le python\n");
    mq_from_py(&snd_buffer);
    printf("packet récupéré\n");
    if (snd_buffer.type == 8)
    {   
        char *minibuf = (char *)malloc(10);
        sprintf(minibuf,"%d",get_save_size());
        memset(snd_buffer.body, 0, sizeof(snd_buffer.body));
        strncpy(snd_buffer.body,minibuf,strlen(minibuf));
        if (send(client2_socket_descriptor, &snd_buffer, sizeof(snd_buffer), 0) < 0)
            stop("Send failed");
        send_pickle_file(client2_socket_descriptor);
    }
    else
    {
        if (send(client2_socket_descriptor, &snd_buffer, sizeof(snd_buffer), 0) < 0)
            stop("Send failed");
    }
    printf("Packet envoyé\n");
    printf("=====================================\n");
}

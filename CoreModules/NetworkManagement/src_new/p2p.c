#include <sys/socket.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "./headers/p2p.h"
#include "./headers/utils.h"
#include "./headers/mq.h"

static packet snd_buffer = {};
static packet rcv_buffer = {};

int first_conn = 0;

char buffer[MAX_SIZE];

void send_pickle_file()
{
    bzero(buffer, MAX_SIZE);
    int file_fd, bytes_read, bytes_sent;

    // Ouvrir le fichier en lecture seule
    file_fd = open("Assets/games/to-send.pkl", O_RDONLY);
    if (file_fd == -1)
    {
        perror("Impossible d'ouvrir le fichier");
        return;
    }

    // Lire le contenu du fichier par blocs de BUFSIZ octets et l'envoyer sur la socket
    while ((bytes_read = read(file_fd, buffer, BUFSIZ)) > 0)
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
    close(first_conn);
}

void receive_picle_file(char *buffer)
// le contenu reçu est directement écris dans le fichier save.pkl dans Assets/game
{
    FILE *file = fopen("save.pkl", "wb"); // ouvrir le fichier en mode binaire
    if (file != NULL)
    {
        fwrite(buffer, sizeof(char), strlen(buffer), file); // écrire le contenu du buffer dans le fichier
        fclose(file);                                       // fermer le fichier
    }
    else
    {
        printf("Impossible d'ouvrir le fichier\n");
    }
}

void p2p_run(char *personal_address, int personal_port, char *client2_address, int client2_port)
{
    printf("\033[1;33m[Setting up personal socket ...]\033[1;0m\n");
    // Creation du socket de reception
    printf("Personal socket : \n");
    int personal_socket_descriptor = socket(AF_INET, SOCK_STREAM, 0);

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
    int process_id = fork();
    if (process_id == 0)
        while (1)
            p2p_handle_rcv(personal_socket_descriptor, (struct sockaddr *)&personal_sock_addr, sock_addr_size);
    else
        while (1)
            p2p_handle_snd(client2_socket_descriptor);
}

void p2p_handle_rcv(int socket_descriptor, struct sockaddr *sock_addr, int sock_addr_size)
{
    fd_set readfds;
    FD_ZERO(&readfds);
    FD_SET(socket_descriptor, &readfds);

    if (select(FD_SETSIZE, &readfds, NULL, NULL, NULL) < 0)
        stop("Select failed");

    for (size_t i = 0; i < FD_SETSIZE; i++)
    {
        if (!FD_ISSET(i, &readfds))
            continue;

        if (i == socket_descriptor)
        {
            printf("acceptation d'un client\n");
            int new_client_socket_descriptor = accept(socket_descriptor, sock_addr, (socklen_t *)&sock_addr_size);
            FD_SET(new_client_socket_descriptor, &readfds);
            first_conn = new_client_socket_descriptor;
        }
        else
        {
            printf("reception d'un packet\n");
            memset(&rcv_buffer, 0, sizeof(packet));
            bzero(buffer, MAX_SIZE);
            int n;
            if ((n = recv(i, buffer, sizeof(buffer), 0)) < 0)
                stop("Recv failed");
            if (buffer[512] == '\0')
            {
                memcpy(&rcv_buffer, buffer, sizeof(packet));
                printf("packet reçu\n");
                FD_CLR(i, &readfds);
                mq_to_py(&rcv_buffer);
            }
            else
            {
                // sauvegarde recu-> ecrire le binaire dans un fichier et envoyer un paquet de type 8 au python pour q'uil charge ce fichier
                receive_picle_file(buffer);
                rcv_buffer.type = 8;
                mq_to_py(&rcv_buffer);
            }
        }
    }
}

void p2p_handle_snd(int client2_socket_descriptor)
{
    memset(&snd_buffer, 0, sizeof(packet));

    mq_from_py(&snd_buffer);
    if (snd_buffer.type == 8)
    {
        send_picle_file();
    }
    else
    {
        if (send(client2_socket_descriptor, &snd_buffer, sizeof(snd_buffer), 0) < 0)
            stop("Send failed");
    }
}
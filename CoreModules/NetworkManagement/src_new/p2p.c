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

void send_pickle_file(char *filename, char *buffer)
{
    FILE *fp;
    fp = fopen(filename, "wb"); // Ouvrir le fichier en mode binaire pour l'écriture
    if (fp == NULL)
    {
        fprintf(stderr, "Impossible d'ouvrir le fichier %s\n", filename);
        exit(EXIT_FAILURE);
    }

    fwrite(buffer, sizeof(char), strlen(buffer), fp); // Écrire le contenu du buffer dans le fichier
    fclose(fp);

    printf("Le contenu du buffer a été écrit dans le fichier %s\n", filename);
}

void receive_picle_file(int server_socket, char *filename)
// le contenu reçu par un recv est directement écris dans le fichier filename
{
    int filefd;
    ssize_t nread;
    char buffer[MAX_SIZE];

    // Ouvrir le fichier en mode écriture, tronquer le fichier s'il existe déjà
    if ((filefd = open(filename, O_WRONLY | O_CREAT | O_TRUNC, 0666)) == -1)
    {
        perror("open");
        exit(EXIT_FAILURE);
    }

    // Réception du fichier bloc par bloc
    while ((nread = recv(server_socket, buffer, MAX_SIZE, 0)) > 0)
    {
        if (write(filefd, buffer, nread) == -1)
        {
            perror("write");
            exit(EXIT_FAILURE);
        }
    }

    // Fermer le fichier
    close(filefd);

    if (nread == -1)
    {
        perror("recv");
        exit(EXIT_FAILURE);
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
            receive_picle_file(new_client_socket_descriptor, "../../../Assets/games/newsauvegarde.pkl");
        }
        else
        {
            printf("reception d'un packet\n");
            memset(&rcv_buffer, 0, sizeof(packet));

            int n;
            if ((n = recv(i, &rcv_buffer, sizeof(rcv_buffer), 0)) < 0)
                stop("Recv failed");

            printf("packet reçu\n");
            FD_CLR(i, &readfds);
            mq_to_py(&rcv_buffer);
        }
    }
}

void p2p_handle_snd(int client2_socket_descriptor)
{
    memset(&snd_buffer, 0, sizeof(packet));

    mq_from_py(&snd_buffer);

    if (send(client2_socket_descriptor, &snd_buffer, sizeof(snd_buffer), 0) < 0)
        stop("Send failed");
    send_pickle_file(client2_socket_descriptor, "../../../Assets/games/sauvegarde.pkl");
}
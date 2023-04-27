#include <sys/socket.h>
#include "sys/select.h"

#ifndef P2P_H
#define P2P_H

#define PACKET_BODY_SIZE 64 - 12
#define MAX_SIZE 2097152

#define DEFAULT 0
#define AJOUTER 1
#define SUPPRIMER 2
#define AJOUT_ROUTE 3
#define SUPPR_ROUTE 4
#define SAUVEGARDE_ASK 5
#define UPDATE 6
#define INIT 7
#define SAUVEGARDE_SEND 8
#define BROADCAST_NEW_PLAYER 9
#define SEND_IP 10



void p2p_run(char *personal_address, int personal_port);
void p2p_handle_rcv(int socket_descriptor, struct sockaddr *sock_addr, int sock_addr_size, fd_set *totalFds);
void p2p_handle_snd();
int p2p_connect_to_other_player(int address, unsigned short port);

typedef struct packet
{
    unsigned short type;
    unsigned short port;
    unsigned int source_address;
    unsigned int destination_address;
    char body[PACKET_BODY_SIZE];
} packet;

#endif
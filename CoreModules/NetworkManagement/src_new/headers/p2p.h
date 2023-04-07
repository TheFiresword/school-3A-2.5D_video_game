#include <sys/socket.h>

#ifndef P2P_H

#define PACKET_BODY_SIZE 2048 - 12
#define MAX_SIZE 2097152

void p2p_run(char *personal_address, int personal_port, char *client2_address, int client2_port);
void p2p_handle_rcv(int socket_descriptor, struct sockaddr *sock_addr, int sock_addr_size);
void p2p_handle_snd();
typedef struct packet
{
    unsigned char type;
    unsigned char pageTotal : 4, pageIndex : 4;
    unsigned short body_size;
    unsigned int source_address;
    unsigned int destination_address;
    char body[PACKET_BODY_SIZE];
} packet;

#endif
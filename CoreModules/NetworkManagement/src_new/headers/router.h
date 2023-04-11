#ifndef ROUTER_H
#define ROUTER_H

#include "p2p.h"

typedef struct Player
{
    unsigned int address;
    unsigned short port;
    int socket;
} Player;

typedef struct listElement
{
    Player player;
    struct listElement *next;
} listElement;

void router_showList();
void router_set_self(Player player);
void router_insertElement(Player player);
void router_send(packet packet);
void router_broadcast(packet packet);
void router_update_set(fd_set *readfds);
int router_get_socket_by_address(unsigned int address, unsigned short port);

#endif
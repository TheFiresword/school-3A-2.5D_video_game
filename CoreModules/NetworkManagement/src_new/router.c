#include <stdio.h>
#include <stdlib.h>
#include <arpa/inet.h>

#include "./headers/router.h"
#include "./headers/utils.h"

static listElement *head = NULL;
static Player self = {};

void router_showList()
{
    printf("Affichage list :\n");
    listElement *current = head;
    while (current != NULL)
    {
        char address[15];
        formatIPAddress(address, current->player.address);
        if (current->player.address == self.address && current->player.port == self.port)
            printf("\033[7m");
        printf("- %s:%d\033[1;0m\n", address, current->player.port);
        current = current->next;
    }
}

int router_get_socket_by_address(unsigned int address, unsigned short port)
{
    listElement *current = head;
    while (current != NULL)
    {
        if (current->player.address == address && current->player.port == port)
        {
            return current->player.socket;
        }
        current = current->next;
    }
    return -1;
}

void router_set_self(Player player)
{
    self = player;
}

void router_insertElement(Player player)
{
    listElement *newListElement = (listElement *)malloc(sizeof(listElement));
    newListElement->player = player;
    newListElement->next = head;
    head = newListElement;
}

void router_send(packet packet)
{
    printf("\033[1;33m[Sending a packet]\033[1;0m\n");

    listElement *current = head;
    while (current != NULL)
    {
        printf("check : %u:%u//%u:%u\n", packet.destination_address, packet.port, current->player.address, current->player.port);
        if (packet.destination_address == current->player.address && packet.port == current->player.port)
        {
            if (send(current->player.socket, &packet, sizeof(packet), 0) < 0)
                stop("Send failed");

            printf("send : %u:%u\n", packet.destination_address, packet.port);

            printf("\033[1;32m[Packet sent]\033[1;0m\n");
            return;
        }

        current = current->next;
    }
    printf("not found : %u:%u\n", packet.destination_address, packet.port );
}

void router_broadcast(packet packet)
{
    printf("\033[1;33m[Sending a broadcast packet]\033[1;0m\n");
    router_showList();

    listElement *current = head;
    while (current != NULL)
    {
        printf("check : %u:%u//%u:%u\n", current->player.address, current->player.port, self.address, self.port);
        if (current->player.address != self.address || current->player.port != self.port)
        {
            if (send(current->player.socket, &packet, sizeof(packet), 0) < 0)
                stop("Send failed");

            printf("send : %u:%u\n", current->player.address, current->player.port);
        }
        current = current->next;
    }

    printf("\033[1;32m[Broadcast end]\033[1;0m\n");
}
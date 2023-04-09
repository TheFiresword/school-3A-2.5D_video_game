#include <sys/msg.h>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>

#include "./headers/p2p.h"
#include "./headers/utils.h"

static int mq_id_from_py = -1;
static int mq_id_to_py = -1;

typedef struct mq_message
{
    long m_type;
    packet packet;
} mq_message;

void mq_setup(int mq_key_from_py, int mq_key_to_py)
{
    printf("\033[1;33m[Setting up message queues ...]\033[1;0m\n");
    mq_id_from_py = msgget(mq_key_from_py, 0666 | IPC_CREAT);
    if (mq_id_from_py < 0)
        stop("Msgget failed");

    printf("\tFrom python message queue id : %d\n", mq_id_from_py);

    mq_id_to_py = msgget(mq_key_to_py, 0666 | IPC_CREAT);
    if (mq_id_to_py < 0)
        stop("Msgget failed");

    printf("\tTo python message queue id : %d\n", mq_id_to_py);

    printf("\033[1;32m[Message queues ok]\033[1;0m\n");
}

void mq_from_py(packet *from_packet)
{

    if (mq_id_to_py < 0)
    {
        printf("[mq_from_py] Invalid message queue id : %d\n", mq_id_to_py);
        exit(1);
    }

    mq_message temp_mq_message = {};

    if (msgrcv(mq_id_from_py, &temp_mq_message, sizeof(packet), 0, 0) == -1)
        stop("Msgrcv failed");

    memcpy(from_packet, &temp_mq_message.packet, sizeof(packet));

    printf("A packet have been received from python\n");
    //printf("message\n");
    //printNHex(sizeof(packet), from_packet);
}

void mq_to_py(packet *to_packet)
{
    if (mq_id_to_py < 0)
    {
        printf("[mq_to_py] Invalid message queue id : %d\n", mq_id_to_py);
        exit(1);
    }

    mq_message temp_mq_message = {.m_type = to_packet->type};

    memcpy(&temp_mq_message.packet, to_packet, sizeof(packet));

    if (msgsnd(mq_id_to_py, &temp_mq_message, sizeof(packet), 0))
        stop("Msgsnd failed");

    printf("A packet have been sent to python\n");
    //printf("message\n");
    //printNHex(sizeof(packet), to_packet);
}
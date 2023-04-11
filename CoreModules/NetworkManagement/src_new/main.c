
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "./headers/p2p.h"
#include "./headers/utils.h"
#include "./headers/mq.h"
#include "./headers/router.h"

int main(int argc, char const *argv[])
{
    if (argc < 5)
    {
        printf("Le ou les arguments ne sont pas valide(s) ou incomplet(s)\n");
        printf("USAGE :\n");
        printf("%s [personal_address] [personal_port] [mq_key_from_py] [mq_key_to_py] [client2_address] [client2_port]\n", argv[0]);
        printf("EXEMPLE :\n");
        printf("%s 127.0.0.1 7000 1234 4321\n", argv[0]);
        exit(EXIT_FAILURE);
    }

    // TODO : Trouver un nom pour décrire toute la partie C
    printf("\033[1;33m[Starting *trouver un nom pour décrire ce truc*]... \033[1;0m\n");
    printf("Using : \n");

    char personal_address[16];
    strncpy(personal_address, argv[1], 16);
    int personal_port = atoi(argv[2]);

    // ==================================================
    // | je pense qu'il est préférable d'utiliser 2 mq  |
    // | pour pouvoir utiliser les memes types de       |
    // | messages pour l'envois et la reception         |
    // ==================================================
    int mq_key_from_py = atoi(argv[3]);
    int mq_key_to_py = atoi(argv[4]);
    printf("\tMessage Queue from python : %d\n\tMessage Queue to python : %d\n", mq_key_from_py, mq_key_to_py);
    printf("\033[1;32m[Initial setup ok]\033[1;0m\n");

    mq_setup(mq_key_from_py, mq_key_to_py);

    p2p_run(personal_address, personal_port);

    return 0;
}

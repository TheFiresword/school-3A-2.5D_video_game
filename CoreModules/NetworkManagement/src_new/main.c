
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "./headers/p2p.h"
#include "./headers/utils.h"
#include "./headers/mq.h"

#define MQ_KEY_FROM_PY 12345
#define MQ_KEY_TO_PY 54321


int main(int argc, char const *argv[])
{
    
    if (argc < 3)
    {
        printf("Le ou les arguments ne sont pas valide(s) ou incomplet(s)\n");
        printf("USAGE :\n");
        printf("%s [personal_address] [personal_port] optional:[client2_address] [client2_port]\n", argv[0]);
        printf("EXEMPLE :\n");
        printf("%s 127.0.0.1 7000 127.0.0.1 7001\n", argv[0]);
        exit(EXIT_FAILURE);
    }


    if (argc > 3 && argc < 5)
    {

        printf("Le ou les arguments ne sont pas valide(s) ou incomplet(s)\n");
        printf("USAGE :\n");
        printf("%s [personal_address] [personal_port] [client2_address] [client2_port]\n", argv[0]);
        printf("EXEMPLE :\n");
        printf("%s 127.0.0.1 7000 1234 4321 127.0.0.1 7001\n", argv[0]);
        exit(EXIT_FAILURE);
    }

    else if(argc == 3 || argc == 5){
        char personal_address[16];
        strncpy(personal_address, argv[1], 16);
        int personal_port = atoi(argv[2]);
        int client2_port = 0;
        char *client2_address = malloc(sizeof(char) * (16+1));

        if(argc == 3){
            //New game
            client2_address = NULL;
        }
        else{
            //Join game
            strncpy(client2_address, argv[3], 16);
            client2_port = atoi(argv[4]);
            printf("\tPersonal : %s:%d\n\tClient2 : %s:%d\n", personal_address, personal_port, client2_address, client2_port);
        }

        printf("\tMessage Queue from python : %d\n\tMessage Queue to python : %d\n", MQ_KEY_FROM_PY, MQ_KEY_TO_PY);
        printf("\033[1;32m[Initial setup ok]\033[1;0m\n");

        mq_setup(MQ_KEY_FROM_PY, MQ_KEY_TO_PY);

        p2p_run(personal_address, personal_port, client2_address, client2_port);
    }

    
    return 0;
}

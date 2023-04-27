#ifndef MQ_H
#define MQ_H

void mq_setup(int mq_key_from_py, int mq_key_to_py);
void mq_to_py(packet *packet);
void mq_from_py(packet *packet);

#endif
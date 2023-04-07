import struct
from enum import IntEnum, unique
from functools import reduce
from typing import Any, Callable, Dict, Tuple, Union

import sysv_ipc

from CoreModules.GameManagement.Update import LogicUpdate

"""
Implementation du protocole definit dans : https://docs.google.com/spreadsheets/d/19Q2D6Y_1bfit8nrRQ_JPPvHSeOotOISHyBvppbNOFP4/edit?usp=sharing
"""


@unique
class PacketTypes(IntEnum):
    Default = 1
    NewPoint = 2


class Packet:
    binPattern: str = "<BH2I501s"
    assert struct.calcsize(binPattern) == 512

    def __init__(
        self,
        body: Union[bytearray, bytes],
        port: int,
        sourceAddress: str,
        destinationAddress: str,
        packetType: Union[int, PacketTypes] = PacketTypes.Default,
        final=False,
    ) -> None:

        self.body = body
        self.port = port
        self.sourceAddress = sourceAddress
        self.destinationAddress = destinationAddress
        self.type: PacketTypes = PacketTypes(packetType)
        self.final = final

    def __str__(self) -> str:
        return f"{self.__class__}\n\ttype : {self.type} {'(final)' if self.final else ''}\n\tport : {self.port}\n\tfrom : {self.sourceAddress}\n\tto  : {self.destinationAddress}"

    @staticmethod
    def addressFromIntAddress(intAddress: int) -> str:
        return f"{intAddress >> 24 & 0xFF}.{intAddress >> 16 & 0xFF}.{intAddress >> 8 & 0xFF}.{intAddress & 0xFF}"

    @staticmethod
    def parseType(type: int) -> Tuple[PacketTypes, bool]:
        return bool(type & 1), type >> 1

    @staticmethod
    def intAddressFromAdress(address: str) -> int:
        return reduce(
            lambda a, b: a | int(b[1]) << (8 * b[0]),
            enumerate(address.split(".")[::-1]),
            0,
        )

    @classmethod
    def unpack(cls, data: Union[bytearray, bytes]):
        (
            packetType,
            port,
            intSourceAddress,
            intDestinationAddress,
            *body,
        ) = struct.unpack(cls.binPattern, data)

        return cls(
            *body,
            port,
            cls.addressFromIntAddress(intSourceAddress),
            cls.addressFromIntAddress(intDestinationAddress),
            *cls.parseType(packetType),
        )

    def generalPack(self, *data):
        return struct.pack(
            self.binPattern,
            self.type.value << 1 | int(self.final),
            self.port,
            self.intAddressFromAdress(self.sourceAddress),
            self.intAddressFromAdress(self.destinationAddress),
            *data,
        )

    def pack(self):
        return self.generalPack(self.body)


def encode_update_packets(update: LogicUpdate):
    MESSAGE_BODY_LIMIT = 501
    packets = []
    update_elements = [
        [update.catchedfire, 1],
        [update.has_evolved, 2],
        [update.collapsed, 3],
    ]

    updateIndex = 0

    while sum(len(update_element) for update_element, _ in update_elements) > 0:
        packetBody = []
        while (
            len(packetBody) + len(update_elements[updateIndex][0]) < MESSAGE_BODY_LIMIT
        ):
            if len(update_elements[updateIndex][0]) == 0:
                updateIndex += 1
                continue

            packetBody += [update_elements[updateIndex][1]] + update_elements[
                updateIndex
            ][0].pop()

            if (
                updateIndex >= len(update_elements)
                or sum(len(update_element) for update_element, _ in update_elements)
                == 0
            ):
                break

        packetBody += [0] * (MESSAGE_BODY_LIMIT - len(packetBody))

        # TODO : generaliser l'adresse et le port
        packets.append(
            Packet(bytearray(packetBody), 8000, "127.0.0.1", "127.0.0.1", final=False)
        )

    packets[-1].final = True
    return packets


class Echange:
    def __init__(self, mq_key_rcv: int, mq_key_snd: int, clear=False) -> None:
        self.mq_rcv = sysv_ipc.MessageQueue(mq_key_rcv, sysv_ipc.IPC_CREAT)
        self.mq_snd = sysv_ipc.MessageQueue(mq_key_snd, sysv_ipc.IPC_CREAT)

        if clear:
            self.emptyMq(self.mq_snd)
            self.emptyMq(self.mq_rcv)

    def emptyMq(self, mq):
        while mq.current_messages > 0:
            mq.receive()

    def send(self, packet: Packet, block: bool = False):
        self.mq_snd.send(packet.pack(), type=packet.type, block=block)

    def receive(self, type: int = 0, block: bool = False):
        data, type = self.mq_rcv.receive(type=type, block=block)
        return Packet.unpack(data)


if __name__ == "__main__":
    p = Packet(b"test", 8000, "127.0.0.1", "127.0.0.1", PacketTypes.Default, True)
    print(p)
    print(p.pack())
    print(Packet.unpack(p.pack()))

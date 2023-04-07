import struct
from enum import IntEnum, unique
from functools import reduce
from typing import Tuple, Union

import sysv_ipc

from CoreModules.GameManagement.Update import LogicUpdate

BODY_SIZE = 512 - 12

"""
Implementation du protocole definit dans : https://docs.google.com/spreadsheets/d/19Q2D6Y_1bfit8nrRQ_JPPvHSeOotOISHyBvppbNOFP4/edit?usp=sharing
"""
 
@unique
class PacketTypes(IntEnum):
    Default = 0
    Ajouter = 1
    Supprimer = 2
    Ajout_Route = 3
    Suppr_Route = 4
    Sauvegarde = 5
    Update = 6
    Init = 7



class Packet:
    binPattern: str = f"<2H2I{BODY_SIZE}s"
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
    def flatten(t):
        out = []
        if type(t) in [list, tuple]:
            for el in t:
                out += flatten(el)
        else:
            out += [t]
        return out

    packets = []
    update_elements = [
        [update.catchedfire, 1],
        [update.has_evolved, 2],
        [update.collapsed, 3],
    ]

    updateIndex = 0

    while sum(len(update_element) for update_element, _ in update_elements) > 0:
        packetBody = []
        while len(packetBody) + len(update_elements[updateIndex][0]) < BODY_SIZE:
            if len(update_elements[updateIndex][0]) == 0:
                updateIndex += 1
                continue

            update_data = flatten(update_elements[updateIndex][0].pop())
            packetBody += [update_elements[updateIndex][1]] + update_data

            if (
                updateIndex >= len(update_elements)
                or sum(len(update_element) for update_element, _ in update_elements)
                == 0
            ):
                break

        packetBody += [0] * (BODY_SIZE - len(packetBody))

        # TODO : generaliser l'adresse et le port
        packets.append(
            Packet(bytearray(packetBody), 9200, "192.168.241.176", "192.168.241.154", final=False, packetType=PacketTypes.Update)
        )
    if len(packets) > 0:
        packets[-1].final = True
    return packets


def decode_update_packets(packet: Packet):
    update_dict = {
        1: [lambda x, y: (x, y), 2],
        2: [lambda x, y, z: ((x, y), z), 3],
        3: [lambda x, y: (x, y), 2],
    }

    updates = [None, [], [], []]

    body = [int(hexa) for hexa in packet.body]

    cursor = 0

    while body[cursor] in update_dict.keys():
        update_id = body[cursor]
        update_factory, update_len = update_dict[update_id]
        cursor += 1

        updates[update_id].append(update_factory(*body[cursor : cursor + update_len]))
        cursor += update_len

    return {
        "catchedfire": updates[1],
        "has_evolved": updates[2],
        "collapsed": updates[3],
    }

def decode_ponctual_packets(packet: Packet):
    
    ponctual_dict = {
        1: [lambda x, y, z: ((x, y), z), 3],
        2: [lambda x, y, z: ((x, y), z), 3],
        3: [lambda x, y, z: ((x, y), z), 3],
        4: [lambda x, y, z: ((x, y), z), 3],
        5: [lambda _: None, 0],
        7: [lambda x, y: (x, y) , 2],
    }

    body = [int(hexa) for hexa in packet.body]
    assert len(body) == ponctual_dict[packet.type][1], f"Packet {packet.type} has a wrong body length"
    return ponctual_dict[packet.type][0](*body)
    
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

    def getter_current_messages(self):
        return (self.mq_rcv.current_messages, self.mq_snd.current_messages)


echanger = Echange(12345, 54321, clear=True)

if __name__ == "__main__":
    p = Packet(b"test", 9200, "127.0.0.1", "127.0.0.1", PacketTypes.Default, True)
    print(p)
    print(p.pack())
    print(Packet.unpack(p.pack()))

dict_demon={1: 'academy',
            2: 'actor_colony',
            3: 'aqueduct',
            4: 'ares_temple', 
            5: 'neptune_temple', 
            6: 'mercury_temple', 
            7: 'mars_temple', 
            8: 'venus_temple', 
            9: 'amphitheater', 
            10: 'barber', 
            11: 'normal_bath', 
            12: 'barracks',
            13: 'clay_pit', 
            14: 'colosseum', 
            15: 'dock', 
            16: 'dwell', 
            17: "engineer's_post", 
            18: 'forum', 
            19: 'fruit_farm', 
            20: 'furniture_workshop', 
            21: 'fort', 
            22: 'fountain', 
            23: 'garden', 
            24: 'gladiator_school', 
            25: 'gov_housing_house',
            26: 'gov_housing_villa', 
            27: 'gov_housing_palace', 
            28: 'granary', 
            29: 'hospital', 
            30: 'iron_mine', 
            31: 'library', 
            32: 'lion_house', 
            33: 'market', 
            34: 'oil_mill', 
            35: 'olive_farm', 
            36: 'oracle', 
            37: 'palace', 
            38: 'perfumery', 
            39: 'police_station', 
            40: 'pottery', 
            41: 'prefecture', 
            42: "proconsul's_palace", 
            43: "procurator's_palace", 
            44: 'quarry', 
            45: 'roadblock', 
            46: 'rock_quarry', 
            47: 'school', 
            48: 'shipyard', 
            49: 'smithy', 
            50: 'statue', 
            51: 'stone_mason', 
            52: 'storage_yard', 
            53: 'tax_office', 
            54: 'teacher', 
            55: 'temple_of_vesta', 
            56: 'theater', 
            57: 'timber_yard', 
            58: 'toolmaker', 
            59: 'townhouse', 
            60: 'trading_post', 
            61: 'trireme_shipyard', 
            62: 'tunnel', 
            63: 'university', 
            64: 'vase_painter', 
            65: 'vintner', 
            66: 'wall',
            67: 'wine_press',
            68: 'workshop'
}

def find_key(value, dict):
    for keys, values in dict.items():
        if values == value:
            return keys
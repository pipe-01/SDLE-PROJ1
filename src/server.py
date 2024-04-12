import asyncio
import time
import random
from warnings import catch_warnings

from src.message import Message, Command
from src.zmq_server import ZMQServer

import pickle

REQUEST_TIMEOUT = 2500

# Ficheiro de backup
topics_file_path = "data/topics.pickle"
offsets_file_path = "data/offsets.pickle"

# offsets = { client1_topic1: 2, client2_topic1: 1, client1_topic2: 3 ... }
try:
    topics_file = open(topics_file_path, 'rb')
    topics = pickle.load(topics_file)
except FileNotFoundError:
    topics_file = open(topics_file_path, 'wb+')
    pickle.dump({}, topics_file)
    topics = {}
topics_file.close()

# ex: topics = { "topic1": (last, {1: value1, 2: value2...}, [clientId1, clientId12] ) }
try:
    offsets_file = open(offsets_file_path, 'rb')
    offsets = pickle.load(offsets_file)
except FileNotFoundError:
    offsets_file = open(offsets_file_path, 'wb+')
    pickle.dump({}, offsets_file)
    offsets = {}
offsets_file.close()

print(topics)
print(offsets)


async def server():
    s1 = ZMQServer()
    await s1.receive(msgProcess)


def msgProcess(msgList):
    msg = Message.listToMessage(msgList)

    ##sleep for test  timeout
    rand = random.randrange(REQUEST_TIMEOUT * 1.10)
    if (rand > REQUEST_TIMEOUT):
        print("timeout error simulation")
        time.sleep(rand / 1000)
        return b"ERROR: timeout simulation"
    topicName = msg.topicName

    if msg.cmd == Command.SUB:
        return processSubscribe(msg, topicName)
    elif msg.cmd == Command.UNSUB:
        return processUnsubscribe(msg, topicName)
    elif msg.cmd == Command.PUT:
        return processPut(msg, topicName)
    elif msg.cmd == Command.GET:
        return processGet(msg, topicName)

    # return None


def processGet(msg, topicName):
    print("GET")
    topic = topics.get(topicName)
    clientId = bytesToString(msg.value)
    if topic is None:  # se ainda nao existe, erro
        return b"ERROR: topic doesn't exist"
    (last, values, clientList) = topic
    if clientId not in clientList:
        return b"ERROR: client is not subscribed"
    else:  # senao, adiciona o clientId no topico
        offset = offsets.get(clientId + "_" + topicName)
        if offset is None:
            return b"ERORR: client is subscribed"
        if last == offset:
            return b"ERROR: client already received all the values available on this topic"
        nextOffset = getNextOffset(last, offset, values)
        offsets[clientId + "_" + topicName] = nextOffset
        print(topics, offsets)
        write_json(offsets_file_path, offsets)
        return stringToBytes(values[nextOffset])


def processPut(msg, topicName):
    print("PUT")
    topic = topics.get(topicName)
    value = bytesToString(msg.value)
    if topic is None:  # se ainda nao existe, eh criado um topico com o elemento
        topics[topicName] = (1, {1: value}, [])
    else:
        (last, values, subs) = topic
        values[last + 1] = value
        topics[topicName] = ((last + 1), values, subs)
    print(topics, offsets)
    write_json(topics_file_path, topics)
    return msg.value


def processUnsubscribe(msg, topicName):
    print("UNSUB")
    clientId = bytesToString(msg.value)
    topic = topics.get(topicName)
    if topic is None:  # se ainda nao existe, eh criado um topico "vazio"
        return b"ERROR: topic does not exists"
    else:  # senao, adiciona o clientId no topico
        (_, _, subs) = topic
        if clientId in subs:
            subs.remove(clientId)
        else:
            return b"ERROR: client is not inscribed"
    del offsets[clientId + "_" + topicName]
    print(topics, offsets)
    write_json(offsets_file_path, offsets)
    return stringToBytes(clientId)


def processSubscribe(msg, topicName):
    print("SUB")
    clientId = bytesToString(msg.value)
    topic = topics.get(topicName)
    if topic is None:  # se ainda nao existe, eh criado um topico "vazio"
        topics[topicName] = (0, {}, [clientId])
    else:  # senao, adiciona o clientId no topico
        (_, _, subs) = topic
        if clientId in subs:
            return b"ERROR: client already inscribed"
        else:
            subs.append(clientId)
    offsets[clientId + "_" + topicName] = topics[topicName][0]
    print(topics, offsets)
    write_json(topics_file_path, topics)
    write_json(offsets_file_path, offsets)
    return stringToBytes(clientId)


def write_json(filename, data):
    with open(filename, 'wb+') as file:
        pickle.dump(data, file)


def getNextOffset(last, offset, values):
    print(offsets)
    print(values)
    value = None
    while offset < last and value is None:
        print(offset)
        offset += 1
        value = values[offset]
    return offset


def stringToBytes(msg):
    return bytes(str(msg), "utf-8")


def bytesToString(bmsg):
    return bmsg.decode("utf-8")


async def main_thread():
    await asyncio.gather(server())


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(main_thread())

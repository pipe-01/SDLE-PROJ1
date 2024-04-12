# SDLE - PROJ 1

## Setup
    python3
    pip install pyzmq


## Run

1. Initiate the Server

```bash
python3 src/server.py
```

2. Run the client
```bash
python3 src/client.py
```

## How to use it

Since there isn't a interface implemented for send messagens it is nescessary to send the messagens in the main() of the client.py with the following format:

![Msg, example msgs in the client.py](/images/client.pyScreenshot.png)

### Mensagens model: 

|   | Message |  |
| --------  | ------------------- | --------------------- |
| GET, SUB, UNSUB | Topics name | Client Id|
| PUT | Topics name | Value for publication (in bytes)  |

Exemples: 
* Subscribe client1 on topic1 
```bash
    Message(Command.SUB, "topic1", "client1").toMultipart()
```
* Unsubscribe client1 on topic1 
```bash
    Message(Command.UNSUB, "topic1", "client1").toMultipart()
```
* Put "Hello Word" on  topic1
```bash
    Message(Command.PUT, "topic1", bytes("Hello Word", "utf-8")).toMultipart()
```
* Request a Get on topic1
```bash
    Message(Command.GET, "topic1", "client1").toMultipart()
```


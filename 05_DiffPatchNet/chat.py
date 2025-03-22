import asyncio
from cowsay import list_cows

clients = {}
clients_names = {}
cows_list = list_cows()


async def chat(reader, writer):
    me = "{}:{}".format(*writer.get_extra_info('peername'))
    print(f'{me} has connected!')
    my_name = ''
    clients[me] = asyncio.Queue()
    send = asyncio.create_task(reader.readline())
    receive = asyncio.create_task(clients[me].get())
    while not reader.at_eof():
        done, _ = await asyncio.wait([send, receive], return_when=asyncio.FIRST_COMPLETED)
        for q in done:
            if q is send:
                send = asyncio.create_task(reader.readline())
                my_msg = q.result().decode().strip().split()
                match my_msg[0]:
                    case 'who':
                        if len(clients_names) == 0:
                            await clients[me].put(f"You're the only cow")
                        else:
                            await clients[me].put(f'{'\n'.join(clients_names.keys())}')
                    case 'cows':
                        cows_avail = set(cows_list).difference(
                            set(clients_names.keys()))
                        await clients[me].put(f'{'\n'.join(cows_avail)}')
                    case 'login':
                        if my_name != '':
                            await clients[me].put(f'You are already a cow!')
                        else:
                            login = my_msg[1]
                            cows_avail = set(cows_list).difference(
                                set(clients_names.keys()))
                            if login in cows_avail:
                                my_name = login
                                clients_names[my_name] = clients[me]
                                await clients[me].put(f"Hello, {my_name}")
                            else:
                                await clients[me].put(f"Please enter valid login!")
                    case _:
                        await clients[me].put(f"Please login first!")
            elif q is receive:
                receive = asyncio.create_task(clients[me].get())
                writer.write(f"{q.result()}\n".encode())
                await writer.drain()
    send.cancel()
    receive.cancel()
    print(me, "DONE")
    del clients[me]
    writer.close()
    await writer.wait_closed()


async def main():
    server = await asyncio.start_server(chat, '0.0.0.0', 1337)
    async with server:
        await server.serve_forever()


asyncio.run(main())

import asyncio
from cowsay import list_cows, cowsay

clients = {}
clients_names = {}
cows_list = list_cows()
command_num = {}


async def chat(reader, writer):
    me = "{}:{}".format(*writer.get_extra_info('peername'))
    print(f'{me} has connected!', flush=True)
    my_name = ''
    quit_flag = 0
    command_num[me] = 0
    clients[me] = asyncio.Queue()
    send = asyncio.create_task(reader.readline())
    receive = asyncio.create_task(clients[me].get())
    while not (reader.at_eof()) and (quit_flag == 0):
        done, _ = await asyncio.wait([send, receive], return_when=asyncio.FIRST_COMPLETED)
        for q in done:
            if q is send:
                send = asyncio.create_task(reader.readline())
                my_msg = q.result().decode().strip().split()
                print(my_msg)
                match my_msg[0]:
                    case 'who':
                        if len(clients_names) == 0:
                            await clients[me].put(f"0:You're the only cow")
                        else:
                            await clients[me].put(f'0:{'\n'.join(clients_names.keys())}')
                    case 'cows':
                        cows_avail = set(cows_list).difference(
                            set(clients_names.keys()))
                        command_num[me] += 1
                        await clients[me].put(f'{command_num[me]}:{'\n'.join(cows_avail)}')
                    case 'quit':
                        quit_flag = 1
                        if my_name != '':
                            clients_names.pop(my_name, None)
                    case 'login':
                        if my_name != '':
                            await clients[me].put(f'0:You are already a cow!')
                        else:
                            login = my_msg[1]
                            cows_avail = set(cows_list).difference(
                                set(clients_names.keys()))
                            if login in cows_avail:
                                my_name = login
                                clients_names[my_name] = clients[me]
                                await clients[me].put(f"0:Hello, {my_name}")
                            else:
                                await clients[me].put(f"0:Please enter valid login!")
                    case 'say':
                        receiver = my_msg[1]
                        if my_name == '':
                            await clients[me].put('0:Login first!')
                        elif (receiver not in list(clients_names.keys())) or (receiver == my_name):
                            await clients[me].put(f"0:Unknown receiver!")
                        else:
                            cow = cowsay(' '.join(my_msg[2:]),
                                         cow=my_name)
                            await clients_names[receiver].put(cow)
                    case 'yield':
                        if my_name == '':
                            await clients[me].put(f"0:Login first!")
                        else:
                            for out in clients.values():
                                if out is not clients[me]:
                                    cow = cowsay(' '.join(my_msg[1:]),
                                                 cow=my_name)
                                    await out.put('0:'+cow)
                    case _:
                        await clients[me].put(f"0:Invalid command!")
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

# Importing
import asyncio
import subprocess

# Placeholder for function to recover nodes recover_node(host, port)
def recover_node(node_number, host, port):
    key_file = "node" + str(node_number)
    subprocess.run(['python3', '-m', 'peer.peer', port, key_file, host, '&'])

# Function to check if a node is alive
async def ping_node(node_number, host, port):
    try:
        reader, writer = await asyncio.open_connection(host, port)
        print(f"Alive node at {host}:{port}")
        writer.close()
        await writer.wait_closed()
    except (OSError, asyncio.TimeoutError):
        print(f"Node at {host}:{port} is not responding")
        # Recover the node using recover_node(host, port) function
        recover_node(node_number, host, port)

# Main Function
async def main():
    peer_file = "peer_list.txt"
    
    peer_list = []
    with open(peer_file, "r") as file:
        for line in file:
            peer_list = line.strip().split(",")

    while True:
        for i in range(len(peer_list)):
            await ping_node(i + 1, "127.0.0.1", peer_list[i][1])
        await asyncio.sleep(5)

if __name__ == "__main__":
    asyncio.run(main())

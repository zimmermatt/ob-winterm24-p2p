#!/usr/bin/env python3

# Importing
import logging
import asyncio
import subprocess

# Logging config
logging.basicConfig(
    filename="supervisor.log",
    filemode="w",
    format="%(asctime)s %(name)s %(levelname)s | %(message)s",
    level=logging.INFO,
)


# Placeholder for function to recover nodes recover_node(host, port)
def recover_node(node_number, host, port):
    key_file = "node" + str(node_number)
    subprocess.run(
        [
            "python3",
            "-m",
            "peer.contributing_peer",
            port,
            key_file,
            host + ":50000",
            "&",
        ]
    )


# Function to check if a node is alive
async def ping_node(node_number, host, port):
    try:
        reader, writer = await asyncio.open_connection(host, port)
        logging.info(f"Alive node at {host}:{port}")
    except (OSError, asyncio.TimeoutError):
        logging.error(f"Node at {host}:{port} is not responding")
        # Recover the node using recover_node(host, port) function
        recover_node(node_number, host, port)
    finally:
        if writer:
            writer.close()
            await writer.wait_closed()


# Main Function
async def main():
    peer_file = "peer_list.txt"

    peer_list = []
    with open(peer_file, "r") as file:
        for line in file:
            peer_list = line.strip().split(",")

    while True:
        for i in range(len(peer_list)):
            await ping_node(i + 1, "0.0.0.0", peer_list[i][1])
        await asyncio.sleep(5)


if __name__ == "__main__":
    asyncio.run(main())

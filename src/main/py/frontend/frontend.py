#!/usr/bin/env python3
"""
Module to manage our frontend

This module allows us to create a GUI for our peer
"""
import asyncio
import logging
import sys
import tkinter as tk
from PIL import ImageTk
from server.network import NotifyingServer as kademlia
from peer.peer import Peer
from utils import call_soon, call_later


class Frontend:
    """Class to manage the frontend of the peer"""

    def __init__(self, peer: Peer):
        """Constructor for the frontend"""
        self.peer: Peer = peer
        self.commission_frames = []

    def create_item_row(self, window, commission):
        """Create a row for a commission in the GUI"""
        frame = tk.Frame(window)
        frame.pack(fill=tk.X)
        self.commission_frames.append(frame)
        label = tk.Label(
            frame,
            text=f"From: {commission.key} |"
            + f"Width: {commission.width} |"
            + f"Height: {commission.height} |"
            + f"Wait Time: {commission.wait_time}",
            width=100,
        )
        label.pack(side=tk.LEFT)
        button = tk.Button(
            frame,
            text="Contribute",
            command=lambda: asyncio.create_task(
                self.peer.contribute_to_artwork(commission)
            ),
        )
        button.pack(side=tk.LEFT)

    def update_commissions(self, window):
        """Update the commission requests in the GUI"""
        # Destroy the old frames
        for frame in self.commission_frames:
            frame.destroy()
        # Get the commission requests from the peer
        commissions = self.peer.commission_requests_received
        # Add each commission request to the listbox
        for commission in commissions:
            # Get the commission details
            self.create_item_row(window, commission)

    def insert_gui_elements(self, window):
        """Create all of the base gui elements"""
        width_label = tk.Label(window, text="Width:")
        width_label.pack()
        width_entry = tk.Entry(window)
        width_entry.pack()

        # Create the height textbox
        height_label = tk.Label(window, text="Height:")
        height_label.pack()
        height_entry = tk.Entry(window)
        height_entry.pack()

        # Create the wait time textbox
        wait_label = tk.Label(window, text="Wait Time:")
        wait_label.pack()
        wait_entry = tk.Entry(window)
        wait_entry.pack()

        button = tk.Button(
            window,
            text="Commission Art Piece",
            command=lambda: self.commission_art_piece(
                width_entry.get(), height_entry.get(), wait_entry.get(), window
            ),
        )
        button.pack()

        # Create the commission requests
        commission_requests_label = tk.Label(window, text="Commission Requests:")
        commission_requests_label.pack()
        self.update_commissions(window)
        self.peer.gui_callback = lambda: self.update_commissions(window)
        self.update_commissions(window)

    def reset_gui(self, window):
        """Reset the GUI to the commission page"""
        # Clear the window
        for widget in window.winfo_children():
            widget.destroy()
            # Create the width textbox
        self.insert_gui_elements(window)

    def commission_art_piece(self, width_entry, height_entry, wait_entry, window):
        """Call commission art piece and display the result in the GUI"""
        width = float(width_entry)
        height = float(height_entry)
        wait_time = float(wait_entry)
        commission = asyncio.create_task(
            self.peer.commission_art_piece(width, height, wait_time, palette_limit=10)
        )
        # Clear the window
        for widget in window.winfo_children():
            widget.destroy()
        # Show a loading animation
        loading_label = tk.Label(window, text="Loading...")
        loading_label.pack()

        async def wait_and_complete(window):
            nonlocal commission
            commission = await commission
            await asyncio.sleep(wait_time)
            loading_label.destroy()
            complete_label = tk.Label(window, text="Commission Complete")
            complete_label.pack()
            image = self.peer.inventory.commission_canvases[commission.key]
            # Resize the image if needed
            image = image.resize((300, 300))
            # Convert the PIL image to a Tkinter-compatible format
            image_tk = ImageTk.PhotoImage(image)
            # Create a Label widget to display the image
            image_label = tk.Label(window, image=image_tk)
            image_label.image = image_tk
            image_label.pack()
            # Add button to reset the gui labelled "Back to commission page"
            reset_button = tk.Button(
                window, text="Reset GUI", command=lambda: self.reset_gui(window)
            )
            reset_button.pack()

        asyncio.create_task(wait_and_complete(window))

    def create_gui(self):
        """Create the GUI for the peer"""
        window = tk.Tk()
        window.geometry("1000x500")

        self.insert_gui_elements(window)

        def update():
            window.update()
            call_later()(0.02, update)

        call_soon()(update)


async def main():
    """Main function

    Run the file with the following:
    python3 frontend.py <port_num> <key_filename> <address>
    """

    logging.basicConfig(
        format="%(asctime)s %(name)s %(levelname)s | %(message)s", level=logging.INFO
    )
    key_filename, port_num = sys.argv[2], int(sys.argv[1])
    address = None
    if len(sys.argv) > 3:
        address = sys.argv[3]
    peer = Peer(port_num, key_filename, address, kademlia)
    await peer.connect_to_network()
    # Create the GUI
    peer_frontend = Frontend(peer)
    peer_frontend.create_gui()
    while True:
        await asyncio.sleep(1)


if __name__ == "__main__":
    asyncio.run(main())

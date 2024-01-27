import tkinter as tk
from tkinter import Label, Canvas, PhotoImage, Listbox, Scrollbar, SINGLE, VERTICAL, StringVar, OptionMenu, Frame, Button, Toplevel, messagebox
import subprocess
import os
import json
import shutil  # Import shutil for directory removal

main = None
server_name_global = None
selected_version_global = None
server_list = []  # Global list to store server names and versions
file_listbox = None

def install_checks():
    try:
        subprocess.run(['java', '-version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        return True
    except subprocess.CalledProcessError:
        return False


def stop_server():
    print("Stopping server...")

def mc_plugins():
    print("Mc plugins")

def create_server():
    global server_list, file_listbox

    # Function to handle the "Create Server" action
    def on_server_creation():
        global server_name_global, selected_version_global
        
        server_name = entry_name.get()  # Get server name from entry widget
        selected_version = server_version_var.get()
        
        server_name_global = server_name
        selected_version_global = selected_version

        # Update server_list with the server details
        server_folder_path = os.path.join("SRC/USERSERVERFILES", server_name)
        os.makedirs(server_folder_path, exist_ok=True)

        server_list.append({"name": server_name, "version": selected_version, "path": server_folder_path})

        # Update the listbox and save the updated server list to a file
        file_listbox.insert("end", f"{server_name} - {selected_version}")
        with open("server_list.json", "w") as file:
            json.dump(server_list, file)

        # Close the frame after server creation
        create_server_frame.destroy()

    # Create a rounded frame for server creation
    create_server_frame = create_rounded_frame(main, "Create Server")

    # Server name entry
    label_name = Label(create_server_frame, text="Enter Server Name:", font=("Arial", 12), bg="white")
    label_name.place(relx=0.5, rely=0.2, anchor="center")
    entry_name = tk.Entry(create_server_frame, font=("Arial", 12), width=20)
    entry_name.place(relx=0.5, rely=0.3, anchor="center")

    # Server version label
    version_label = Label(create_server_frame, text="Select Server Version", font=("Arial", 12), bg="white")
    version_label.place(relx=0.5, rely=0.5, anchor="center")

    # Server version options
    server_versions = ["1.17", "1.16.5", "1.15.2"]  # Add your desired versions
    server_version_var = StringVar()
    server_version_var.set(server_versions[0])  # Set default version

    version_menu = OptionMenu(create_server_frame, server_version_var, *server_versions)
    version_menu.config(font=("Arial", 12), bg="white")
    version_menu.place(relx=0.5, rely=0.7, anchor="center")

    # Button to confirm server creation
    confirm_button = Button(create_server_frame, text="Create Server", command=on_server_creation, font=("Arial", 12), bg="lightgreen")
    confirm_button.place(relx=0.5, rely=0.9, anchor="center")

    # Button to close the "Create Server" frame
    close_button = Button(create_server_frame, text="Close", command=create_server_frame.destroy, font=("Arial", 12), bg="salmon")
    close_button.place(relx=0.5, rely=1.1, anchor="center")
    
    
def start_server():
    server_file = "SRC/" + server_name_global + "/" + selected_version_global + ".jar"
    print(server_file)
    
    
def main_window():
    global main, server_list, file_listbox  # Declare main, server_list, and file_listbox as global variables
    main = tk.Tk()
    main.title("MCX Dashboard")
    main.geometry("800x600")

    title_font = ("Arial", 16, "bold")

    java_installed = install_checks()

    if not java_installed:
        welcome_text = Label(main, text="Java is not installed. Please install Java first.", font=title_font, fg="red")
        welcome_text.pack(pady=40, padx=60)

        # Wait for 5 seconds before exiting
        main.after(5000, main.destroy)
    else:
        # Sidebar with icons
        sidebar = Canvas(main, width=100, height=600, bg="lightgray")
        sidebar.pack(side="left", fill="both")

        # Load icons (adjust the file paths accordingly)
        plus_icon = PhotoImage(file="SRC/IMAGES/plus.png")
        start_icon = PhotoImage(file="SRC/IMAGES/start.png")
        stop_icon = PhotoImage(file="SRC/IMAGES/stop2.png")
        plugin_icon = PhotoImage(file="SRC/IMAGES/mcpluginslogo.png")
        delete_icon = PhotoImage(file="SRC/IMAGES/delete.png")  # Add your delete icon image path

        # Draw icons on the sidebar
        sidebar.create_image(50, 50, anchor="center", image=plus_icon, tags="create_server")
        sidebar.create_image(50, 150, anchor="center", image=start_icon, tags="start_server")
        sidebar.create_image(50, 250, anchor="center", image=stop_icon, tags="stop_server")
        sidebar.create_image(50, 350, anchor="center", image=plugin_icon, tags="mc_plugins")
        sidebar.create_image(50, 450, anchor="center", image=delete_icon, tags="delete_server")  # Add delete icon

        # Set up events for each icon
        sidebar.tag_bind("create_server", "<Button-1>", lambda event: handle_add_server())
        sidebar.tag_bind("start_server", "<Button-1>", lambda event: start_server())
        sidebar.tag_bind("stop_server", "<Button-1>", lambda event: stop_server())
        sidebar.tag_bind("mc_plugins", "<Button-1>", lambda event: mc_plugins())
        sidebar.tag_bind("delete_server", "<Button-1>", lambda event: delete_selected_server())  # Bind delete function

        main_text = Label(main, text="MCX Server Dashboard", font=title_font)
        main_text.pack()

        # Scrollable area to display file names
        file_listbox = Listbox(main, selectmode=SINGLE, font=("Arial", 12), exportselection=0, height=20)
        file_listbox.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        # Add a scrollbar to the listbox
        scrollbar = Scrollbar(main, orient=VERTICAL, command=file_listbox.yview)
        scrollbar.pack(side="right", fill="y")
        file_listbox.config(yscrollcommand=scrollbar.set)

        # Load server list from file or create an empty list
        try:
            with open("server_list.json", "r") as file:
                server_list = json.load(file)
        except FileNotFoundError:
            server_list = []

        # Insert server names into the listbox
        for server in server_list:
            file_listbox.insert("end", f"{server['name']} - {server['version']}")

    main.mainloop()

def create_rounded_frame(parent, title):
    frame = Frame(parent, bg="white", bd=4)
    frame.place(relx=0.5, rely=0.5, anchor="center")

    # Rounded frame with a black border
    canvas = tk.Canvas(frame, bg="white", width=300, height=200, highlightthickness=5, highlightbackground="black")
    canvas.pack()

    # Title
    title_label = Label(canvas, text=title, font=("Arial", 12), bg="white")
    title_label.place(relx=0.5, rely=0.1, anchor="center")

    return frame

def handle_add_server():
    # Function to handle the "Add Server" action

    def on_server_creation():
        server_name = entry_name.get()  # Get server name from entry widget
        selected_version = server_version_var.get()

        # Create a folder for the Minecraft server
        src_file = f"SRC/SERVERFILES/{selected_version}.jar"
        destination_directory = f"SRC/USERSERVERFILES/{server_name}"
        new_name = f"{server_name}.jar"

        try:
            # Check if the source file exists
            if not os.path.exists(src_file):
                raise FileNotFoundError(f"Source file not found: {src_file}")

            # Create the destination directory if it doesn't exist
            os.makedirs(destination_directory, exist_ok=True)

            # Copy the source file to the destination with the new name
            shutil.copy2(src_file, os.path.join(destination_directory, new_name))

            print(f"File cloned and renamed from {os.path.basename(src_file)} to {new_name} in {destination_directory}")

            # Update server_list with the server details, including the 'path' key
            server_folder_path = os.path.abspath(destination_directory)
            server_list.append({"name": server_name, "version": selected_version, "path": server_folder_path})

            # Update the listbox and save the updated server list to a file
            file_listbox.insert("end", f"{server_name} - {selected_version}")
            with open("server_list.json", "w") as file:
                json.dump(server_list, file)

            # Close the frame after server creation
            add_server_frame.destroy()

        except Exception as e:
            print(f"Error during server creation: {e}")


    # Create a rounded frame for aesthetics within the main window
    add_server_frame = create_rounded_frame(main, "Add Server")

    # Server name entry
    label_name = Label(add_server_frame, text="Enter Server Name:", font=("Arial", 12), bg="white")
    label_name.place(relx=0.5, rely=0.2, anchor="center")
    entry_name = tk.Entry(add_server_frame, font=("Arial", 12), width=20)
    entry_name.place(relx=0.5, rely=0.3, anchor="center")

    # Server version label
    version_label = Label(add_server_frame, text="Select Server Version", font=("Arial", 12), bg="white")
    version_label.place(relx=0.5, rely=0.5, anchor="center")

    # Server version options
    server_versions = ["1.20.4 (LATEST)", "1.20.3", "1.20.2", "1.20.1", "1.20"]  # Add your desired versions
    server_version_var = StringVar()
    server_version_var.set(server_versions[0])  # Set default version

    version_menu = OptionMenu(add_server_frame, server_version_var, *server_versions)
    version_menu.config(font=("Arial", 12), bg="white")
    version_menu.place(relx=0.5, rely=0.7, anchor="center")

    # Button to confirm server version selection
    confirm_button = Button(add_server_frame, text="Confirm", command=on_server_creation, font=("Arial", 12), bg="lightgreen")
    confirm_button.place(relx=0.35, rely=0.9, anchor="center")

    # Button to close the "Add Server" frame
    close_button = Button(add_server_frame, text="Close", command=add_server_frame.destroy, font=("Arial", 12), bg="salmon")
    close_button.place(relx=0.65, rely=0.9, anchor="center")

def delete_selected_server():
    selected_index = file_listbox.curselection()
    if selected_index:
        # Get the selected server details
        selected_server = server_list[selected_index[0]]
        server_name = selected_server["name"]

        # Display a confirmation popup
        confirmation = messagebox.askquestion("Confirmation", f"Are you sure you want to delete {server_name}?")
        if confirmation == 'yes':
            # Remove the server from the listbox
            file_listbox.delete(selected_index)

            # Remove the server folder and update the server list
            shutil.rmtree(selected_server["path"])
            server_list.remove(selected_server)

            # Save the updated server list to a file
            with open("server_list.json", "w") as file:
                json.dump(server_list, file)

# Call the main_window function directly
main_window()

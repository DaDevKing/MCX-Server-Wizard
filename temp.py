from tkinter import *
from tkinter import ttk
import subprocess

java_installed = False

def install_checks():
    global java_installed
    try:
        subprocess.run(['java', '-version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        java_installed = True
    except subprocess.CalledProcessError:
        java_installed = False

def main_window():
    main = Tk()
    main.title("MCX Dashboard")
    main.geometry("700x450")
    main.config(bg="#ECECEC")  # Set background color

    title_font = ("Arial", 16, "bold")
    font_color = "#333"  # Dark gray color

    install_checks()

    if not java_installed:
        welcome_text = Label(main, text="Java is not installed. Please install Java first.", font=title_font, fg="red", bg="#ECECEC")
        welcome_text.pack(pady=40, padx=60)

        # Wait for 5 seconds before exiting
        main.after(5000, main.destroy)
    else:
        def new_server_GUI():
            selected_version = version_var.get()
            print("Selected Minecraft Version:", selected_version)

        # Dropdown menu for Minecraft versions
        version_var = StringVar(main)
        version_var.set("Select Version")  # Default text

        versions = ["1.8.9", "1.12.2", "1.16.5", "1.17.1"]  # Add more versions as needed
        version_menu = OptionMenu(main, version_var, *versions)
        version_menu.config(font=(title_font[0], title_font[1]), fg=font_color, bg="#ECECEC")  # Set font, text color, and background color
        version_menu.grid(row=0, column=0, padx=10, pady=10, sticky="nw")

        new_server = Button(main, text="Select", font=title_font, fg=font_color, bg="#4CAF50", command=new_server_GUI)  # Green button
        new_server.grid(row=1, column=0, padx=10, pady=10, sticky="nw")

    main.mainloop()

# Call the main_window function directly
main_window()

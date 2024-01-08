import os
import sys
from tktooltip import ToolTip
import subprocess
import webbrowser
from tkinter import *
from ctypes import windll
from app_library import apps
from PIL import Image, ImageTk
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
# pyinstaller --add-data 'app_library.py;.' --add-data 'app_launcher.ico;.' --add-data 'Read Me.txt;.' --exclude-module app_library --icon=app_launcher.ico app_launcher3.pyw --contents-directory .

windll.shcore.SetProcessDpiAwareness(1)

####################################################  App Editor  ####################################################
def game_editor():
    root.destroy()
    python = sys.executable
    button_delete_list = []
    button_edit_list = []

#### Delete Game Tab ####

    def ui_delete_game():
        button_delete.grid_remove()
        button_add.grid()
        button_edit.grid()

        def delete_game(app_name):
            op = messagebox.askyesno("Delete App", "Do you really want to delete" + app_name)
            if op > 0:
                apps.pop(app_name, None)
                update_apps_file()

        def update_apps_file():
            with open("app_library.py", "w") as file:
                file.write(f"apps = {{" + "")
                for app_name, app_data in apps.items():
                    file.write(f"\n    '{app_name}':{{'path':r'{app_data['path']}','icon':r'{app_data['icon']}','option':r'{app_data['option']}'}},")
                file.write(f"\n}}")
            subprocess.Popen([python, r"app_launcher3.pyw"])
            window.destroy()

        ### Generate Button for apps that will be deleted ###

        app_items = list(apps.items())
        for app_name, app_data in app_items:
            try:
                icon = Image.open(app_data['icon'])
            except FileNotFoundError:
                icon = Image.open("app_launcher.ico")
            icon = icon.resize((32, 32))
            icon = ImageTk.PhotoImage(icon)
            lebardelete = lebar * (9/10)
            button = Button(master=window, text=f" Delete   {app_name}", image=icon, compound='left', anchor="w",
                        width=lebardelete, command=lambda line_to_delete=app_name: delete_game(line_to_delete))
            button.image = icon
            button.grid(column=0, columnspan=5, padx=10, pady=5)
            button_delete_list.append(button)

        ### Window configuration based on Apps count ###

        if window.winfo_screenheight() == 1080:
            tambahan4=74
            if len(apps.items()) > 3:
                tambahan = len(apps.items())
                tambahan2 = 42
            elif len(apps.items()) <= 3:
                tambahan = 3
                tambahan2 = 57
        else:
            tambahan4=53
            if len(apps.items()) > 3:
                tambahan = len(apps.items())
                tambahan2 = 30
            elif len(apps.items()) <= 3:
                tambahan = 3
                tambahan2 = 41

        tambahan3 = tambahan2+(tambahan * tambahan4)
        window.geometry(f"{lebar}x{tambahan3}+250+100")

#### Add Game Tab ####

    def ui_add_game():
        button_add.grid_remove()
        button_delete.grid()
        button_edit.grid()
        #info = None
        type_icon = [("Image files", ("*.jpg", "*.jpeg", "*.png", "*.ico")),("All files", "*.*")]
        type_game = [("App files", "*.exe"),("Python files",("*.py","*.pyw")),("All files", "*.*")]

        def browse_game(entry,type):
            path = askopenfilename(filetypes=type)
            entry.delete(0,END)
            entry.insert(0,path)

        def input_game():
            if len(ui_add_game.lokasi_entry.get()) == 0 or len(ui_add_game.gambar_entry.get()) == 0:
                messagebox.showerror("Error", "Don't leave Location and Icon entries empty", type=messagebox.OKCANCEL)

            else:
                with open("app_library.py", "r+") as file:
                    judul = ui_add_game.judul_entry.get()
                    lokasi = ui_add_game.lokasi_entry.get()                    
                    gambar = ui_add_game.gambar_entry.get()
                    opsi = ui_add_game.opsi_entry.get()
                    judul = judul.replace('\\', '/')
                    lokasi = lokasi.replace('\\', '/')
                    gambar = gambar.replace('\\', '/')
                    judul = judul.strip()
                    lokasi = lokasi.strip()
                    gambar = gambar.strip()
                    opsi = opsi.strip()
                    if len(gambar) == 0:
                        gambar = "icon"
                    else:
                        pass
                    lines = file.readlines()
                    lines.insert(-1, ("    ' " + judul + "': {'path':r'" + lokasi +"','icon':r'" + gambar + "','option':r'" + opsi +"'}," + "\n"))
                    file.seek(0)
                    file.writelines(lines)
                    file.truncate()
                    subprocess.Popen([python, r"app_launcher3.pyw"])
                    window.destroy()

        ### Add Game Form ###
        def clear_entry(entry):
            if entry.get() == "Title" or entry.get() == "Location" or entry.get() == "Icon":
                entry.delete(0, END)

        ui_add_game.judul_label = Label(master=window, text="Title", anchor="w", compound="left")
        ui_add_game.judul_label.grid(row=1, column=0, columnspan=1)

        ui_add_game.judul_entry = Entry(master=window, bg="white", width=30)
        ui_add_game.judul_entry.grid(row=1, column=1, columnspan=4)
        ui_add_game.judul_entry.insert(0, "Title")
        ui_add_game.judul_entry.bind("<FocusIn>", lambda event, entry=ui_add_game.judul_entry: clear_entry(entry))

        ui_add_game.lokasi_label = Label(master=window, text="Location", anchor="w", compound='left')
        ui_add_game.lokasi_label.grid(row=3, column=0, columnspan=1)

        ui_add_game.lokasi_entry = Entry(master=window, bg="white", width=30)
        ui_add_game.lokasi_entry.grid(row=3, column=1, columnspan=4)
        ui_add_game.lokasi_entry.insert(0, "Location")
        ToolTip(ui_add_game.lokasi_entry, msg="Fill with application\nor Steam app\nor Website\nor Python script\nor Text file")
        ui_add_game.lokasi_entry.bind("<FocusIn>", lambda event, entry=ui_add_game.lokasi_entry: clear_entry(entry))

        ui_add_game.lokasi_button = Button(master=window, text="Browse", command=lambda: browse_game(ui_add_game.lokasi_entry,type_game))
        ui_add_game.lokasi_button.grid(row=3, column=5)

        ui_add_game.opsi_label = Label(master=window, text="Option", anchor="w", compound='left')
        ui_add_game.opsi_label.grid(row=4, column=0, columnspan=1)

        ui_add_game.opsi_entry = Entry(master=window, bg="white", width=30)
        ui_add_game.opsi_entry.grid(row=4, column=1, columnspan=4)
        ToolTip(ui_add_game.opsi_entry, msg="Leave it empty\nif you don't know")

        ui_add_game.gambar_label = Label(master=window, text="Icon", anchor="w", compound='left')
        ui_add_game.gambar_label.grid(row=2, column=0, columnspan=1)

        ui_add_game.gambar_entry = Entry(master=window, bg="white", width=30)
        ui_add_game.gambar_entry.grid(row=2, column=1, columnspan=4)
        ui_add_game.gambar_entry.insert(0, "Icon")
        ui_add_game.gambar_entry.bind("<FocusIn>", lambda event, entry=ui_add_game.gambar_entry: clear_entry(entry))

        ui_add_game.gambar_button = Button(master=window, text="Browse", command=lambda: browse_game(ui_add_game.gambar_entry,type_icon))
        ui_add_game.gambar_button.grid(row=2, column=5)

        ui_add_game.input_button = Button(master=window, text="Input", anchor='w', command=lambda: input_game())
        ui_add_game.input_button.grid(row=5, column=4)
            
        window.geometry(f"{lebar}x{tinggi}+250+100")

#### Edit Game Tab ####

    def ui_edit_game():
        button_edit.grid_remove()
        button_delete.grid()
        button_add.grid()
        def edit_game(a,b,c,d):
            def input_game(a):
                if len(ui_edit_game.lokasi_entry.get()) == 0 or len(ui_edit_game.gambar_entry.get()) == 0:
                    messagebox.showerror("Error", "Don't leave Location and Icon entries empty", type=messagebox.OKCANCEL)
                else:
                    apps.pop(a, None)

                    with open("app_library.py", "w") as file:
                        file.write(f"apps = {{" + "")
                        for app_name, app_data in apps.items():
                            file.write(f"\n    '{app_name}':{{'path':'{app_data['path']}','icon':'{app_data['icon']}','option':r'{app_data['option']}'}},")
                        file.write(f"\n}}")
                
                    with open("app_library.py", "r+") as file:
                        judul = ui_edit_game.judul_entry.get()
                        lokasi = ui_edit_game.lokasi_entry.get()                    
                        gambar = ui_edit_game.gambar_entry.get()
                        opsi = ui_edit_game.opsi_entry.get()
                        judul = judul.replace('\\', '/')
                        lokasi = lokasi.replace('\\', '/')
                        gambar = gambar.replace('\\', '/')
                        judul = judul.strip()
                        lokasi = lokasi.strip()
                        gambar = gambar.strip()
                        opsi = opsi.strip()
                        if len(gambar) == 0:
                            gambar = "icon"
                        else:
                            pass
                        lines = file.readlines()
                        lines.insert(-1, ("    ' " + judul + "': {'path':r'" + lokasi +"','icon':r'" + gambar + "','option':r'" + opsi +"'}," + "\n"))
                        file.seek(0)
                        file.writelines(lines)
                        file.truncate()
                        subprocess.Popen([python, r"app_launcher3.pyw"])
                        window.destroy()
            type_icon = [("Image files", ("*.jpg", "*.jpeg", "*.png", "*.ico")),("All files", "*.*")]
            type_game = [("App files", "*.exe"),("Python files",("*.py","*.pyw")),("All files", "*.*")]
            def browse_game(a,b):
        
                path = askopenfilename(filetypes=b)
                a.delete(0,END)
                a.insert(0,path)
            for button in button_edit_list:
                button.grid_remove()

            ### Form To Edit Selected App ###

            ui_edit_game.judul_label = Label(master=window, text="Title", anchor="w", compound="left")
            ui_edit_game.judul_label.grid(row=1, column=0)

            ui_edit_game.judul_entry = Entry(master=window, bg="white", width=30)
            ui_edit_game.judul_entry.grid(row=1, column=1, columnspan=4)
            ui_edit_game.judul_entry.insert(0, a)

            ui_edit_game.lokasi_label = Label(master=window, text="Location", anchor="w", compound='left')
            ui_edit_game.lokasi_label.grid(row=3, column=0)

            ui_edit_game.lokasi_entry = Entry(master=window, bg="white", width=30)
            ui_edit_game.lokasi_entry.grid(row=3, column=1, columnspan=4)
            ui_edit_game.lokasi_entry.insert(0, b)

            ui_edit_game.lokasi_button = Button(master=window, text="Browse", command=lambda: browse_game(ui_edit_game.lokasi_entry,type_game))
            ui_edit_game.lokasi_button.grid(row=3, column=5)

            ui_edit_game.gambar_label = Label(master=window, text="Icon", anchor="w", compound='left')
            ui_edit_game.gambar_label.grid(row=2, column=0)

            ui_edit_game.gambar_entry = Entry(master=window, bg="white", width=30)
            ui_edit_game.gambar_entry.grid(row=2, column=1, columnspan=4)
            ui_edit_game.gambar_entry.insert(0, c)

            ui_edit_game.gambar_button = Button(master=window, text="Browse", command=lambda: browse_game(ui_edit_game.gambar_entry,type_icon))
            ui_edit_game.gambar_button.grid(row=2, column=5)

            ui_edit_game.opsi_label = Label(master=window, text="Options", anchor="w", compound='left')
            ui_edit_game.opsi_label.grid(row=4, column=0)

            ui_edit_game.opsi_entry = Entry(master=window, bg="white", width=30)
            ui_edit_game.opsi_entry.grid(row=4, column=1, columnspan=4)
            ui_edit_game.opsi_entry.insert(0, d)

            ui_edit_game.cancel_button = Button(master=window, text="cancel", anchor="w", command=lambda: [ui_edit_game(), remove_edit(2)])
            ui_edit_game.cancel_button.grid(row=5, column=3)
            ui_edit_game.input_button = Button(master=window, text="Input", anchor='w', command=lambda: input_game(a))
            ui_edit_game.input_button.grid(row=5, column=4)
        
        ### Generate button for Apps that will be Edited ###

        app_items = list(apps.items())
        for app_name, app_data in app_items:
            try:
                icon = Image.open(app_data['icon'])
            except FileNotFoundError:
                icon = Image.open("app_launcher.ico")
            icon = icon.resize((32, 32))
            icon = ImageTk.PhotoImage(icon)

            button = Button(master=window, text=f" Edit       {app_name}", image=icon, compound='left', anchor="w",
                            width=300, command=lambda name= app_name, path = app_data['path'], image=app_data["icon"], option=app_data["option"]: edit_game(name,path,image,option))
            button.image = icon
            button.grid(column=0, columnspan=5, padx=10, pady=5)
            button_edit_list.append(button)

        ### Window Size Configuration ###

        if window.winfo_screenheight() == 1080:
            tambahan4=74
            if len(apps.items()) > 3:
                tambahan = len(apps.items())
                tambahan2 = 42
            elif len(apps.items()) <= 3:
                tambahan = 3
                tambahan2 = 57
        else:
            tambahan4=53
            if len(apps.items()) > 3:
                tambahan = len(apps.items())
                tambahan2 = 30
            elif len(apps.items()) <= 3:
                tambahan = 3
                tambahan2 = 41

        tambahan3 = tambahan2+(tambahan * tambahan4)
        window.geometry(f"{lebar}x{tambahan3}+250+100")

#### Buttons Remove Section ####

    ### Remove Buttons Except Add ###

    def remove_add():
        button_delete.grid()
        button_edit.grid()
        button_add.grid_remove()
        for button in button_delete_list:
            button.grid_remove()
        for button in button_edit_list:
            button.grid_remove()
        ui_edit_game.judul_label.grid_remove()
        ui_edit_game.judul_entry.grid_remove()
        ui_edit_game.lokasi_label.grid_remove()
        ui_edit_game.lokasi_entry.grid_remove()
        ui_edit_game.gambar_label.grid_remove()
        ui_edit_game.gambar_entry.grid_remove()
        ui_edit_game.input_button.grid_remove()
        ui_edit_game.lokasi_button.grid_remove()
        ui_edit_game.gambar_button.grid_remove()
        ui_edit_game.cancel_button.grid_remove()
        #ui_edit_game.info.grid_remove()
    
    ### Remove Buttons Except Delete ###

    def remove_delete():
        button_delete.grid_remove()
        button_add.grid()
        button_edit.grid()
        for button in button_edit_list:
            button.grid_remove()
        grid_add_list = [ui_add_game.judul_label, 
                         ui_add_game.judul_entry, 
                         ui_add_game.lokasi_label, 
                         ui_add_game.lokasi_entry, 
                         ui_add_game.gambar_label, 
                         ui_add_game.gambar_entry, 
                         ui_add_game.input_button, 
                         ui_add_game.lokasi_button, 
                         ui_add_game.gambar_button,
                         ui_add_game.opsi_label, 
                         ui_add_game.opsi_entry]
        for grid in grid_add_list:
            grid.grid_remove()
        grid_edit_list = [ui_edit_game.judul_label, 
                          ui_edit_game.judul_entry, 
                          ui_edit_game.lokasi_label, 
                          ui_edit_game.lokasi_entry, 
                          ui_edit_game.gambar_label, 
                          ui_edit_game.gambar_entry, 
                          ui_edit_game.input_button, 
                          ui_edit_game.lokasi_button, 
                          ui_edit_game.gambar_button,
                          ui_edit_game.cancel_button,
                          ui_edit_game.opsi_label, 
                          ui_edit_game.opsi_entry]
        for grid in grid_edit_list:
            grid.grid_remove()

        #ui_edit_game.info.grid_remove()

    ### Remove Button Except Edit ###

    def remove_edit(a):
        if a == 1:
            button_edit.grid_remove()
            button_add.grid()
            button_delete.grid()
            for button in button_delete_list:
                button.grid_remove()
            ui_add_game.judul_label.grid_remove()
            ui_add_game.judul_entry.grid_remove()
            ui_add_game.lokasi_label.grid_remove()
            ui_add_game.lokasi_entry.grid_remove()
            ui_add_game.gambar_label.grid_remove()
            ui_add_game.gambar_entry.grid_remove()
            ui_add_game.input_button.grid_remove()
            ui_add_game.lokasi_button.grid_remove()
            ui_add_game.gambar_button.grid_remove()
            ui_add_game.opsi_label.grid_remove()
            ui_add_game.opsi_entry.grid_remove()
        else:
            grid_edit_list = [ui_edit_game.judul_label, 
                          ui_edit_game.judul_entry, 
                          ui_edit_game.lokasi_label, 
                          ui_edit_game.lokasi_entry, 
                          ui_edit_game.gambar_label, 
                          ui_edit_game.gambar_entry, 
                          ui_edit_game.input_button, 
                          ui_edit_game.lokasi_button, 
                          ui_edit_game.gambar_button,
                          ui_edit_game.cancel_button,
                          ui_edit_game.opsi_entry,
                          ui_edit_game.opsi_label]
            for grid in grid_edit_list:
                grid.grid_remove()


    ### App Editor Window Configuration ###

    window = Tk()
    window.title("App Input")
    window.resizable(False, False)

    window.iconbitmap('app_launcher.ico')

    if window.winfo_screenheight() == 1080:
        lebar = 500
        tinggi = 280
        menu = 30
        intent = 42
    else:
        lebar = 330
        tinggi = 180
        menu = 22
        intent = 30
    window.geometry(f"{lebar}x{tinggi}+250+100")

    ### App Editor Form ###

    label_add = Label(master=window, width=14, text="Add Game")
    label_add.grid(row=0, column=0, columnspan=2, sticky="nsew")
    button_add = Button(master=window,width=14, text="Add Game", command=lambda: [ui_add_game(), remove_add()])
    button_add.grid(row=0, column=0, columnspan=2, sticky="nsew")

    label_delete = Label(master=window, width=14, text="Delete Game")
    label_delete.grid(row=0, column=2, columnspan=2, sticky="nsew")
    button_delete = Button(master=window, width=14, text="Delete Game", command=lambda: [ui_delete_game(), remove_delete()])
    button_delete.grid(row=0, column=2, columnspan=2, sticky="nsew")

    label_edit = Label(master=window, width=14, text="Edit Game")
    label_edit.grid(row=0, column=4, columnspan=2, sticky="nsew")
    button_edit = Button(master=window, width=14, text="Edit Game", command=lambda: [ui_edit_game(), remove_edit(1)])
    button_edit.grid(row=0, column=4, columnspan=2, sticky="nsew")

    
    
    def close():
        subprocess.Popen([python, r"app_launcher3.pyw"])
        window.destroy()
    window.protocol("WM_DELETE_WINDOW", close)
    ui_add_game()
    window.mainloop()

####################################################  App Launcher  ####################################################

python = sys.executable
def launch_app(app_path, options):
    if app_path.endswith('.exe'):
        if os.path.isfile(app_path) == TRUE:
            folder_path , file_name = os.path.split(app_path)
            import subprocess
            option = options.split()
            app = [app_path] + option

            subprocess.Popen(app, cwd=folder_path)
            root.destroy()
        else:
            result = messagebox.showerror("error", '     App file not found.\n\n     try to Edit or Delete the App!', type=messagebox.OKCANCEL)
            if result == messagebox.OK:
                game_editor()
            else:
                subprocess.Popen([python,r'app_launcher3.pyw'])

    elif app_path.startswith('steam://') or app_path.startswith('https://') or app_path.startswith('http://'):
        webbrowser.open(app_path, new=2)

    elif app_path.endswith('.pyw') or app_path.endswith('.py'):
        if os.path.isfile(app_path) == TRUE:
            subprocess.Popen([python,app_path])
            root.destroy()
        else:
            result = messagebox.showerror("error", '     file not found.\n\n     try to Edit or Delete it!', type=messagebox.OKCANCEL)
            if result == messagebox.OK:
                game_editor()
            else:
                subprocess.Popen([python,r'app_launcher3.pyw'])

    elif app_path.endswith('.txt'):
        if os.path.isfile(app_path) == TRUE:
            subprocess.run(['start', 'notepad', app_path], shell=True)
            root.destroy()
        else:
            result = messagebox.showerror("error", '     file not found.\n\n     try to Edit or Delete it!', type=messagebox.OKCANCEL)
            if result == messagebox.OK:
                game_editor()
            else:
                subprocess.Popen([python,r'app_launcher3.pyw'])

    else:
        result = messagebox.showerror("error", '     Unsupported file type.\n\n     Delete App?', type=messagebox.OKCANCEL)
        if result == messagebox.OK:
            game_editor()
        else:
            subprocess.Popen([python,r'app_launcher3.pyw'])

    root.destroy()

root = Tk()
root.title('Apps')
root.iconbitmap('app_launcher.ico')
root.resizable(False, False)
if root.winfo_screenheight() == 1080:
    lebarlauncher=280
else:
    lebarlauncher=200

app_items = apps.items()
app_items_sorted = sorted(app_items, key=lambda x: x[0])
for app_name, app_data in app_items_sorted:
    try:
        icon = Image.open(app_data['icon'])
    except FileNotFoundError:
        icon = Image.open("app_launcher.ico")
    icon = icon.resize((32, 32))
    icon = ImageTk.PhotoImage(icon)
    button = Button(root, text=app_name, image=icon, compound='left', anchor="w",
                       width=lebarlauncher, command=lambda app_path=app_data['path'], options=app_data['option']: launch_app(app_path,options))
    button.image = icon 
    button.pack(padx=10, pady=5)

icon = Image.open('app_launcher.ico')
icon = icon.resize((32, 32))
icon = ImageTk.PhotoImage(icon)
button = Button(root, text='Edit App', image=icon, compound='left', anchor="w",
                   width=lebarlauncher, command=lambda : game_editor())
button.image = icon 
button.pack(padx=10, pady=5)
root.mainloop()

import tkinter as tk
from tkinter import ttk, filedialog
import threading
import os


stop_event = threading.Event()


patterns_for_read = ['.txt', '.csv', '.json', '.log', '.cfg', '.md', '.ini', '.conf', '.html', '.xml', 
                     '.css', '.js', '.php', '.py', '.java', '.c', '.cpp', '.sql', '.bat', '.sh', '.report', 
                     '.yaml', '.toml', '.env', '.tsv']


def search_files(start_dir, keyword, pattern, listbox):
    listbox.delete(0, tk.END)
    try:
        for root, dirs, files in os.walk(start_dir):
            if stop_event.is_set():
                print("Search stopped.")
                break
            for file in files:
                if stop_event.is_set():
                    break
                file_path = os.path.join(root, file)
                if pattern == '':
                    if keyword.lower() in file.lower():
                        listbox.insert(tk.END, file_path)
                        listbox.update()
                        continue
                else:
                    if keyword.lower() in file.lower() and file.endswith(pattern):
                        listbox.insert(tk.END, file_path)
                        listbox.update()
                        continue
                if (pattern in patterns_for_read) and file.endswith(pattern) and var.get() == 1:
                    try:
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            if keyword.lower() in f.read().lower():
                                listbox.insert(tk.END, file_path)
                                listbox.update()
                    except Exception as e:
                        print(f"Error reading file {file_path}: {e}")
    except Exception as e:
        print(f"Error while searching: {e}")


def choose_directory():
    selected_directory = filedialog.askdirectory()
    if selected_directory:
        entry_path.delete(0, tk.END)
        entry_path.insert(0, selected_directory)



def start_search():
    stop_event.clear()
    start_dir = entry_path.get()
    keyword = entry_keyword.get()
    pattern = entry_pattern.get()
    if os.path.exists(start_dir):
        threading.Thread(target=search_files, args=(start_dir, keyword, pattern, listbox), daemon=True).start()
    else:
        listbox.delete(0, tk.END)
        listbox.insert(tk.END, "Source does not exist!")


def stop_search():
    stop_event.set()


def open_file(event):
    try:
        file_path = listbox.get(listbox.curselection())
        if os.path.isfile(file_path):
            os.startfile(file_path)
        else:
            listbox.insert(tk.END, "It's not a file")
    except IndexError:
        pass


window = tk.Tk()
window.title("File Search")


var = tk.IntVar()


frame = ttk.Frame(window, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E))


ttk.Label(frame, text="Путь:").grid(row=0, column=0, sticky=tk.W)
entry_path = ttk.Entry(frame, width=50)
entry_path.grid(row=0, column=1)
entry_path.insert(0, "C:\\" if os.name == "nt" else "/")

btn_browse = ttk.Button(frame, text="Обзор...", command=choose_directory)
btn_browse.grid(row=0, column=2, padx=5)


ttk.Label(frame, text="Pattern:").grid(row=1, column=0, sticky=tk.W)
entry_pattern = ttk.Entry(frame, width=50)
entry_pattern.grid(row=1, column=1)
entry_pattern.insert(0, ".txt")


ttk.Label(frame, text="Keyword:").grid(row=2, column=0, sticky=tk.W)
entry_keyword = ttk.Entry(frame, width=50)
entry_keyword.grid(row=2, column=1)
entry_keyword.insert(0, "")


btn_start = ttk.Button(frame, text="Start Searching", command=start_search)
btn_start.grid(row=3, column=0, pady=10)


btn_stop = ttk.Button(frame, text="Stop Searching", command=stop_search)
btn_stop.grid(row=3, column=1, pady=10)

check_button = tk.Checkbutton(
    window,
    text="Seacrh in files",
    variable=var
)
check_button.grid(row=2, column=0, sticky=tk.W)


listbox = tk.Listbox(window, width=100, height=30)
listbox.grid(row=1, column=0, sticky=(tk.W, tk.E))
listbox.bind("<Double-1>", open_file)

window.mainloop()
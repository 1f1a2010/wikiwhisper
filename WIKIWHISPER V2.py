import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog # so file saving can be better
import wikipediaapi as wk
import pyttsx3 as py
import threading
import re


# Initialize root window
root = tk.Tk()
root.geometry("600x500")
root.title("wikiwhisper")

# Configure grid layout
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=2)


# Label at the top
label = tk.Label(root, text="WIKIWISPER", font=('Verdane', 16))
label.grid(row=0, column=0, columnspan=2, pady=10)

# Entry field for input
entry = tk.Entry(root, width=40, font=('Arial', 14))
entry.grid(row=1, column=0, padx=7,sticky='e')

toggle_theme_btn = tk.Button(root, text="🌙 Toggle Dark Mode", font=('Arial', 12), command=lambda: toggle_theme())
toggle_theme_btn.grid(row=6, column=1, padx=10, pady=10, columnspan=4, sticky='e')
# Search button
btn_1 = tk.Button(root, text="Search", width=10, height=1, command=lambda:threading.Thread(target=get_input).start())
btn_1.grid(row=1, column=1, padx=5,sticky='w')

# Text field to show summary
field = tk.Text(root, height=10, width=60, font=('Arial', 12), wrap='word')
field.grid(row=2, column=0, columnspan=2, padx=10, pady=10,sticky='ew')

# Label to show what user entered
result_label = tk.Label(root, text="", font=('Arial', 12))
result_label.grid(row=3, column=0, columnspan=2, pady=5)

# Read More button (gets longer summary)
read_btn = tk.Button(root, text="🔎 Read More", font=('Arial', 12), command=lambda: threading.Thread(target=read_more).start())

aloud_btn = tk.Button(root, text="READ ALOUD", font=('Arial', 12), command=lambda: threading.Thread(target=readloud).start())

scrllbar = tk.Scrollbar(root, orient='vertical', command=field.yview)
scrllbar.grid(row=2, column=2, sticky='ns')
field.config(yscrollcommand=scrllbar.set)

# Exit button
exit_btn = tk.Button(root, text="Exit", width=10, command=root.destroy)
exit_btn.grid(row=4, column=1, sticky='e', padx=20, pady=10)

save_btn = tk.Button(root, text="💾 Save Summary", font=('Arial', 12), command=lambda: save())

readstop_btn = tk.Button(root, text="STOP", font=('Arial', 12), command=lambda: stopread())


# Function to get summary and show in field
def get_input():
    global last_topic
    user_input = entry.get()
    if not user_input.strip():
        messagebox.showwarning("Input Error", "Please enter a topic to search.")
        return
    else:
        last_topic = user_input
        root.after(0,lambda:result_label.config(text="You entered: " + user_input))
        try:
            wiki = wk.Wikipedia(language='en', extract_format=wk.ExtractFormat.WIKI, user_agent='WikiWhisper/1.0')
            page = wiki.page(user_input)
            if not page.exists():
                root.after(0,lambda:result_label.config(text="Page not found. Try being more specific."))
                return
            else:
                # summary = page.summary[:500]
               
                summary=re.findall(r'[^.!?]+[.!?]', page.summary)
                summary=" ".join(summary[:3])  

                root.after(0,lambda:field.delete('1.0', tk.END))
                root.after(0,lambda:field.insert(tk.END, summary))
                root.after(0,lambda:read_btn.grid(row=4, column=0, padx=10, pady=10, sticky='w'))
                root.after(0,lambda:aloud_btn.grid(row=5, column=0, padx=11, pady=11, sticky='w'))
                root.after(0,lambda:save_btn.grid(row=5, column=1, padx=10, pady=10, sticky='e'))
        except Exception as e:
            root.after(0,lambda:field.delete('1.0', tk.END))
            root.after(0,lambda:result_label.config(text=str(e)))

def read_more():
    try:
        if last_topic:
            wiki = wk.Wikipedia(language='en', extract_format=wk.ExtractFormat.WIKI, user_agent='WikiWhisper/1.0')
            page = wiki.page(last_topic)
            if not page.exists():
                root.after(0,lambda:result_label.config(text="Page not found."))
                return
            summary =re.findall(r'[^.!?]+[.!?]', page.summary)
            summary=" ".join(summary[:7])
            root.after(0,lambda:field.delete('1.0', tk.END))
            root.after(0,lambda:field.insert(tk.END, summary))
            root.after(0,lambda:result_label.config(text=f"Showing more details for: {last_topic}"))
           
    except Exception as e:
        root.after(0,lambda:field.delete('1.0', tk.END))
        root.after(0,lambda:result_label.config(text=str(e)))
    
    
 
    
def readloud():
    text = field.get("1.0", tk.END).strip()
    if text:
        root.after(0,lambda:readstop_btn.grid(row=6, column=0, padx=10, pady=10, sticky='w'))
        root.after(0,lambda:result_label.config(text="Reading aloud..."))
        def speak():
            try:
                engine = py.init()
                engine.say(text)
                engine.runAndWait()
                root.after(0,lambda:readstop_btn.grid_remove())
            except Exception as e:
                result_label.config(text=f"❗Error: {e}")
        threading.Thread(target=speak).start()



def stopread():
    engine = py.init()
    engine.stop()
    root.after(0,lambda:result_label.config(text="Reading stopped."))

def save():
    text = field.get("1.0", tk.END).strip()
    if text:
        space_remo = re.sub('\s+', ' ', text).strip()  # Remove extra whitespace

        sentences = re.findall(r'[^.!?]+[.!?]', space_remo)
        formatted_text = "\n".join(s.strip() for s in sentences if s.strip())

        filename = filedialog.asksaveasfilename(defaultextension=".txt")
        if not filename:
            root.after(0,lambda:result_label.config(text="❗Save cancelled."))
            return
        else:
         with open(filename, "w", encoding="utf-8") as file:
            file.write(formatted_text + "\n")
         root.after(0,lambda:result_label.config(text=f"✅ Summary saved as {filename}"))
    else:
        root.after(0,lambda:result_label.config(text="❗No text to save."))


def apply_theme(theme):
    root.configure(bg=theme["bg"])
    label.config(bg=theme["bg"], fg=theme["fg"])
    entry.config(bg=theme["entry_bg"], fg=theme["entry_fg"], insertbackground=theme["fg"])
    field.config(bg=theme["text_bg"], fg=theme["text_fg"])
    result_label.config(bg=theme["bg"], fg=theme["fg"])
    scrllbar.config(bg=theme["bg"])

    # Update all buttons
    for button in [btn_1, read_btn, save_btn, aloud_btn, readstop_btn, exit_btn, toggle_theme_btn]:
        button.config(bg=theme["entry_bg"], fg=theme["fg"], activebackground=theme["bg"], activeforeground=theme["fg"])


def toggle_theme():
    global dark_mode
    dark_mode = not dark_mode
    theme = DARK_THEME if dark_mode else LIGHT_THEME
    apply_theme(theme)


# Start with empty topic
last_topic = ""
dark_mode = False
# Run the app
LIGHT_THEME = {
    "bg": "white",
    "fg": "black",
    "entry_bg": "white",
    "entry_fg": "black",
    "text_bg": "white",
    "text_fg": "black",
}

DARK_THEME = {
    "bg": "#2e2e2e",
    "fg": "white",
    "entry_bg": "#3c3c3c",
    "entry_fg": "white",
    "text_bg": "#3c3c3c",
    "text_fg": "white",
}

root.mainloop()
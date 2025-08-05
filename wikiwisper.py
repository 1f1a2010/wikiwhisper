import tkinter as tk
import wikipedia as wk
import pyttsx3 as py
engine=py.init()
# Initialize root window
root = tk.Tk()
root.geometry("600x500")
root.title("Wikipedia Summary App")

# Configure grid layout
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)

# Label at the top
label = tk.Label(root, text="WIKIWISPER", font=('Verdane', 16))
label.grid(row=0, column=0, columnspan=2, pady=10)

# Entry field for input
entry = tk.Entry(root, width=40, font=('Arial', 14))
entry.grid(row=1, column=0, padx=10, pady=10)

# Search button
btn_1 = tk.Button(root, text="Search", width=10, height=1, command=lambda: get_input())
btn_1.grid(row=1, column=1, padx=5)

# Text field to show summary
field = tk.Text(root, height=10, width=60, font=('Arial', 12), wrap='word')
field.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

# Label to show what user entered
result_label = tk.Label(root, text="", font=('Arial', 12))
result_label.grid(row=3, column=0, columnspan=2, pady=5)

# Read More button (gets longer summary)
read_btn = tk.Button(root, text="🔎 Read More", font=('Arial', 12), command=lambda: read_more())
read_btn.grid(row=4, column=0, padx=10, pady=10, sticky='w')

aloud_btn = tk.Button(root,text ="READ ALOUD",font=('Arial',12),command=lambda:readloud())
aloud_btn.grid(row=5,column=0,padx=11,pady=11,sticky='w')
# Exit button
exit_btn = tk.Button(root, text="Exit", width=10, command=root.destroy)
exit_btn.grid(row=4, column=1, sticky='e', padx=20, pady=10)

save_btn = tk.Button(root, text="💾 Save Summary", font=('Arial', 12), command=lambda:save())
save_btn.grid(row=5, column=1, padx=10, pady=10, sticky='e')


# Function to get summary and show in field
def get_input():
    global last_topic
    user_input = entry.get()
    last_topic = user_input  # store last searched topic
    result_label.config(text="You entered: " + user_input)
    try:
        summary = wk.summary(user_input, sentences=2)
        field.delete('1.0', tk.END)
        field.insert(tk.END, summary)
    except Exception as e:
        field.delete('1.0', tk.END)
        field.insert(tk.END, f"Error: {e}")

# Function to fetch a longer summary of same topic
def read_more():
    try:
        if last_topic:
            summary = wk.summary(last_topic, sentences=5)
            field.delete('1.0', tk.END)
            field.insert(tk.END, summary)
    except Exception as e:
        field.delete('1.0', tk.END)
        field.insert(tk.END, f"Error: {e}")


def readloud():
    text = field.get("1.0", tk.END).strip()
    if text:
        engine.say(text)
        engine.runAndWait()
# Global file counter to avoid overwriting files
save_counter = 1

def save():
    global save_counter
    text = field.get("1.0", tk.END).strip()
    if text:
        filename = f"summary_{save_counter}.txt"
        with open(filename, "w", encoding="utf-8") as file:
            file.write(text)
        result_label.config(text=f"✅ Summary saved as {filename}")
        save_counter += 1
    else:
        result_label.config(text="❗No text to save.")
   

# Start with empty topic
last_topic = ""

# Run the app
root.mainloop()

import tkinter as tk
from tkinter import messagebox
import time
import random
from PIL import Image, ImageTk  


SAMPLE_TEXTS = [
    "Your school is the institution you owe so much to. As a child you enter into school in kindergarten, and it is your teacher who teaches you the alphabets and the numbers in class.",
    "War has been a part of human existence for thousands of years. It has been fought for varying reasons such as conquests, power, ideology, and religion.",
    "Practice can make everything possible for a man and make them perfect on regular practice in any area. We must know the importance of practice in our daily life especially students",
]

# Virtual Keyboard Layout
KEYBOARD_LAYOUT = [
    "qwertyuiop",
    "asdfghjkl",
    "zxcvbnm"
]

class TypingSpeedTestApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Typing Speed Test")
        self.root.geometry("1000x700")
        self.root.configure(bg="#F5F5F5")  
        self.bg_image = Image.open(r"C:\Users\MY-PC\Desktop\aditya\background.jpg")
        self.bg_image = self.bg_image.resize((1000, 700)) 

        self.bg_image = self.bg_image.convert("RGBA") 
        width, height = self.bg_image.size
        pixels = self.bg_image.load()

        
        for y in range(height):
            for x in range(width):
                r, g, b, a = pixels[x, y]
                a = int(a * 0.3)
                pixels[x, y] = (r, g, b, a)

        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

       
        self.sample_text = ""
        self.start_time = None
        self.input_text = tk.StringVar()
        self.correct_words = 0
        self.total_words = 0
        self.time_limit = 60 
        self.time_left = self.time_limit
        self.timer_running = False

    
        self.create_menu_page()

    def create_menu_page(self):
        self.clear_screen()

        # background
        bg_label = tk.Label(self.root, image=self.bg_photo)
        bg_label.place(relwidth=1, relheight=1)

        
        tk.Label(self.root, text="Welcome to the Typing Speed Test!", font=("Helvetica", 24, "bold"),
                 bg="#F5F5F5", fg="#333333", padx=10, pady=20).pack(pady=50)

        
        self.create_mode_button("Practice Mode", self.practice_mode, "#4CAF50", "#45A049")
        self.create_mode_button("Challenge Mode", self.challenge_mode, "#FF5733", "#FF471A")
        self.create_mode_button("Exit", self.root.quit, "#E74C3C", "#D62C1A")

    def create_mode_button(self, text, command, color, hover_color):
        button = tk.Button(self.root, text=text, font=("Helvetica", 18, "bold"), bg=color, fg="white", relief="flat",
                           activebackground=color, command=command, height=2, width=20, bd=0, padx=10, pady=10)
        button.pack(pady=10)

        
        button.bind("<Enter>", lambda event, button=button, hover_color=hover_color: button.config(bg=hover_color))
        button.bind("<Leave>", lambda event, button=button, color=color: button.config(bg=color))

    def practice_mode(self):
        self.show_typing_screen("Practice Mode")

    def challenge_mode(self):
        self.show_typing_screen("Challenge Mode", timer=True)

    def show_typing_screen(self, mode, timer=False):
        """Create the typing screen."""
        self.clear_screen()
        bg_label = tk.Label(self.root, image=self.bg_photo)
        bg_label.place(relwidth=1, relheight=1)

        self.sample_text = random.choice(SAMPLE_TEXTS)
        self.correct_words = 0
        self.total_words = 0
        self.input_text.set("")
        self.timer_running = timer
        self.time_left = self.time_limit
        tk.Label(self.root, text=mode, font=("Helvetica", 20, "bold"), bg="#F5F5F5", fg="#333333").pack(pady=10)
        self.displayed_text = tk.Text(self.root, font=("Consolas", 18), height=4, bg="#F5F5F5", fg="#333333", bd=0, wrap="word")
        self.displayed_text.pack(pady=20)
        self.displayed_text.insert("1.0", self.sample_text)
        self.displayed_text.config(state="disabled")

  
        self.input_field = tk.Entry(self.root, textvariable=self.input_text, font=("Consolas", 18), bg="#FFFFFF",
                                    fg="#333333", relief="flat", bd=1)
        self.input_field.pack(pady=10, ipadx=5, ipady=5)
        self.input_field.bind("<space>", self.check_word)
        self.input_field.bind("<Key>", self.key_pressed)  
        self.input_field.focus()

        self.output_text = tk.Text(self.root, font=("Consolas", 18), height=4, bg="#F5F5F5", fg="#333333", bd=0, wrap="word")
        self.output_text.pack(pady=20)
        self.output_text.config(state="disabled")

        self.key_labels = {}
        for row in KEYBOARD_LAYOUT:
            frame = tk.Frame(self.root, bg="#F5F5F5")
            frame.pack()
            for char in row:
                key_label = tk.Label(frame, text=char.upper(), font=("Consolas", 18), bg="#FFFFFF", fg="#333333",
                                     width=3, height=2, relief="flat", bd=1)
                key_label.pack(side="left", padx=2, pady=2)
                self.key_labels[char] = key_label  

        if self.timer_running:
            self.timer_label = tk.Label(self.root, text=f"Time Left: {self.time_left}s", font=("Consolas", 16), bg="#F5F5F5", fg="blue")
            self.timer_label.pack(pady=10)
            self.update_timer()

    def key_pressed(self, event):
        """Handle key press and blink corresponding key."""
        char = event.char.lower()
        if char in self.key_labels:
            key_label = self.key_labels[char]
            key_label.config(bg="lightblue") 
            self.root.after(200, lambda: key_label.config(bg="#FFFFFF")) 

    def check_word(self, event):
        """Check word and update feedback."""
        user_input = self.input_text.get().strip()
        words = self.sample_text.split()

        if self.total_words < len(words):
            correct_word = words[self.total_words]
            feedback = f"{user_input} ✔" if user_input == correct_word else f"{user_input} ❌"

            self.output_text.config(state="normal")
            self.output_text.insert(tk.END, feedback + " ")
            self.output_text.config(state="disabled")


            if user_input == correct_word:
                self.correct_words += 1
            self.total_words += 1

            self.input_text.set("")

        if self.total_words >= len(words):
            self.input_field.config(state="disabled")
            self.end_test()

    def update_timer(self):
        """Update the countdown timer."""
        if self.time_left > 0:
            self.time_left -= 1
            self.timer_label.config(text=f"Time Left: {self.time_left}s")
            self.root.after(1000, self.update_timer)
        else:
            self.input_field.config(state="disabled")
            self.end_test()

    def end_test(self):
        """Display the test result."""
        messagebox.showinfo("Test Complete", f"Correct Words: {self.correct_words}/{self.total_words}")

    def clear_screen(self):
        """Clear all widgets from the root window."""
        for widget in self.root.winfo_children():
            widget.destroy()

# Main Execution
if __name__ == "__main__":
    root = tk.Tk()
    app = TypingSpeedTestApp(root)
    root.mainloop()

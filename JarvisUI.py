import tkinter as tk

class JarvisGUI:
    def __init__(self, master):
        self.master = master
        master.title("Jarvis Assistant")

        # Create frames
        self.input_frame = tk.Frame(master)
        self.input_frame.pack(fill="x")

        self.output_frame = tk.Frame(master)
        self.output_frame.pack(fill="both", expand=True)

        # Create input field
        self.input_field = tk.Entry(self.input_frame, width=50)
        self.input_field.pack(side="left", fill="x", expand=True)

        # Create send button
        self.send_button = tk.Button(self.input_frame, text="Send", command=self.send_input)
        self.send_button.pack(side="right")

        # Create output text box
        self.output_text = tk.Text(self.output_frame)
        self.output_text.pack(fill="both", expand=True)

    def send_input(self):
        input_text = self.input_field.get()
        self.input_field.delete(0, "end")

        # Process input text
        if re.search('weather|temperature', input_text):
            city = input_text.split(' ')[-1]
            get_weather(city)
            self.output_text.insert("end", f"Weather in {city}:\n")
            self.output_text.insert("end", get_weather(city) + "\n")

        elif re.search('news', input_text):
            get_news()
            self.output_text.insert("end", "News:\n")
            self.output_text.insert("end", get_news() + "\n")

        elif re.search('play music', input_text):
            play_music()
            self.output_text.insert("end", "Playing music...\n")

        elif re.search('joke', input_text):
            tell_joke()
            self.output_text.insert("end", "Joke:\n")
            self.output_text.insert("end", tell_joke() + "\n")

        elif re.search('define', input_text):
            word = input_text.split(' ')[-1]
            get_definition(word)
            self.output_text.insert("end", f"Definition of {word}:\n")
            self.output_text.insert("end", get_definition(word) + "\n")

        elif re.search('exit', input_text):
            self.master.destroy()

        else:
            self.output_text.insert("end", "I didn't understand that. Please try again.\n")

root = tk.Tk()
my_gui = JarvisGUI(root)
root.mainloop()
import tkinter as tk
from tkinter import scrolledtext, END, simpledialog, messagebox
import nltk
from nltk.chat.util import Chat, reflections
import json

nltk.download('punkt')

class ChatbotGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("ChatBuddy")

        # Create Chatbot instance
        self.chatbot = Chat(pairs, reflections)
        self.user_responses = self.load_user_responses()

        # Get screen width and height
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()

        x_position = int((screen_width - 870) / 2)  # Assuming a width of 800
        y_position = int((screen_height - 680) / 2)  # Assuming a height of 600

        # Set the geometry of the window
        self.master.geometry(f"800x600+{x_position}+{y_position}")

        # Create and configure the text widget
        self.chat_display = scrolledtext.ScrolledText(master, wrap=tk.WORD, width=75, height=25, font=("Helvetica", 12))
        self.chat_display.pack(pady=10)
        self.chat_display.config(state=tk.DISABLED)

        # Create the entry widget for user input
        self.user_input = tk.Entry(master, width=40, font=("Helvetica", 12))
        self.user_input.pack(pady=10)

        # Bind the <Return> key to the send_message function
        self.user_input.bind('<Return>', lambda event=None: self.send_message())

        # Set the focus on the input panel
        self.user_input.focus_set()

        self.master.configure(bg='#F0FFFF')  # Set background color for the main window
        self.chat_display.configure(bg='#FFFFFF')  # Set background color for the chat display
        self.user_input.configure(bg='#FFFFFF')  # Set background color for the user input field

        self.send_button = tk.Button(master, text="Send", command=self.send_message, font=("Helvetica", 12),
                                     bg='#FFFFFF', fg='#0000FF')
        self.send_button.pack(pady=10)

        # Load chat history from a file
        self.load_chat_history()

        # Display a welcome message
        self.display_message("Bot: Welcome to ChatBuddy! How can I help you today?")

    def load_user_responses(self):
        try:
            with open("user_responses.json", "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    def save_user_responses(self):
        with open("user_responses.json", "w") as file:
            json.dump(self.user_responses, file, indent=2)

    def load_chat_history(self):
        try:
            with open("chat_history.txt", "r") as file:
                chat_history = file.read()
                self.chat_display.insert(tk.END, chat_history)
        except FileNotFoundError:
            pass

    def save_chat_history(self, message):
        with open("chat_history.txt", "a") as file:
            file.write(message + "\n")

    def send_message(self):
        user_input_text = self.user_input.get().strip()
        self.user_input.delete(0, END)

        if not user_input_text:
            messagebox.showwarning("Warning", "Input field cannot be empty.")
            return

        if user_input_text.lower() == 'quit':
            self.master.destroy()
        else:
            response = self.get_chatbot_response(user_input_text)
            user_message = "You: " + user_input_text
            bot_message = "Bot: " + response
            self.display_message(user_message)
            self.display_message(bot_message)

            # Save the messages to the chat history
            self.save_chat_history(user_message)
            self.save_chat_history(bot_message)

    def get_chatbot_response(self, user_input_text):
        return self.get_learned_response(user_input_text) or self.chatbot.respond(user_input_text)

    def get_learned_response(self, user_input_text):
        learned_response = self.user_responses.get(user_input_text.lower())

        if not learned_response:
            user_response = self.ask_user_for_response(user_input_text)
            if user_response:
                self.user_responses[user_input_text.lower()] = user_response
                self.save_user_responses()
                return user_response

        return learned_response

    def ask_user_for_response(self, user_input_text):
        response = simpledialog.askstring("Learn Response", f"I don't know the answer. Please tell me what to say when asked '{user_input_text}'?")
        if response:
            confirm = messagebox.askyesno("Confirm Response", f"Do you want to save this response: '{response}'?")
            if confirm:
                return response
        return None

    def display_message(self, message):
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, message + "\n")
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)

if __name__ == "__main__":
    pairs = [
        [r"hey", ["Hello! What's up?"]],
        [r"hello", ["Hey! How's everything going?"]],
        [r"hello (.*)", ["Hello %1! How may I help you today?"]],
        [r"what do you do", ["I'm ChatBuddy, here to have a conversation with you."]],
        [r"my name is (.*)", ["Hello %1! How can I help you today?"]],
        [r"what is your name?", ["My name is ChatBuddy."]],
        [r"how are you ?", ["I'm doing well, thank you!"]],
        [r"sorry (.*)", ["Apologies are not needed. How can I assist you?"]],
        [r"(.*) (good|great|fine)", ["That's wonderful to hear!", "I'm glad you're doing well."]],
        [r"quit", ["Goodbye! Have a great day."]],
        [r"what are you doing", ["Just trying to learn new things."]],
        [r"(.*)", ["I'm sorry, I didn't understand that."]]
    ]

    root = tk.Tk()
    chatbot_gui = ChatbotGUI(root)
    root.mainloop()

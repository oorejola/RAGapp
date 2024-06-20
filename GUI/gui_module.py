# gui_module.py

import tkinter as tk
from tkinter import scrolledtext
from RAG import rag_response 

class AIResponseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("RAG")

        # Variable to store conversation history
        self.conversation_history = ""

        # Create user input text area
        self.user_input_text = tk.Text(self.root, height=5, width=50)
        self.user_input_text.insert(tk.END, "Type your message here...")
        self.user_input_text.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        
        # Bind events for placeholder behavior
        self.user_input_text.bind("<FocusIn>", self.on_entry)
        self.user_input_text.bind("<FocusOut>", self.on_leave)

        # Create submit button
        self.submit_button = tk.Button(self.root, text="Submit", command=self.on_submit)
        self.submit_button.grid(row=0, column=1, padx=10, pady=10)

        # Create response text area
        self.response_text = scrolledtext.ScrolledText(self.root, state=tk.DISABLED, height=15, width=70)
        self.response_text.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        self.response_text.tag_config("user", foreground="SpringGreen3")
        self.response_text.tag_config("user_response", foreground="black")
        self.response_text.tag_config("ai", foreground="SlateBlue4")
        self.response_text.tag_config("ai_thinking", foreground="gray64")
        self.response_text.tag_config("ai_response", foreground="black")
        
        # Configure grid resizing behavior
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=0)

    def on_entry(self, event):
        if self.user_input_text.get("1.0", tk.END).strip() == "Type your message here...":
            self.user_input_text.delete("1.0", tk.END)

    def on_leave(self, event):
        if self.user_input_text.get("1.0", tk.END).strip() == "":
            self.user_input_text.insert(tk.END, "Type your message here...")

    def on_submit(self):
        user_input = self.user_input_text.get("1.0", tk.END).strip()
        if user_input and user_input != "Type your message here...":
            # Update conversation history
            self.conversation_history += f"User: {user_input}\n"
            
            # Display the user input in the response text area in green
            self.response_text.config(state=tk.NORMAL)
            self.response_text.insert(tk.END, "User: ", "user")
         # Insert the actual user input with the response tag
            self.response_text.insert(tk.END, f"{user_input}\n", "user_response")
            
            # Indicate AI is thinking
            self.response_text.insert(tk.END, "AI: ","ai")
            self.response_text.insert(tk.END, "I'm thinking...\n","ai_thinking")
            self.response_text.config(state=tk.DISABLED)
            self.response_text.see(tk.END)

            # Clear the user input text area
            self.user_input_text.delete("1.0", tk.END)

            # Delay the AI response by 1 seconds (1000 milliseconds)
            self.response_text.after(1000, self.get_ai_response)

        else:
            self.user_input_text.delete("1.0", tk.END)
            self.user_input_text.insert(tk.END, "Type your message here...")

    def get_ai_response(self):
        # Get the AI response
        ai_response = rag_response(self.conversation_history)
        
        # Update conversation history with AI response
        self.conversation_history += f"agent: {ai_response}\n"
        
        # Remove the "I'm thinking..." text and insert the actual response
        self.response_text.config(state=tk.NORMAL)
        self.response_text.delete("end-2l", "end-1l")  # Remove the "I'm thinking..." line
        self.response_text.insert(tk.END, "AI: ","ai")
        self.response_text.insert(tk.END, f"{ai_response}\n","ai_response")
        self.response_text.config(state=tk.DISABLED)
        self.response_text.see(tk.END)






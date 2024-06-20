# main.py

from tkinter import Tk
from GUI import AIResponseApp
import os

def main():
    root = Tk()
    app = AIResponseApp(root)
    root.mainloop()

if __name__ == "__main__":

    # Set OpenAI API key
    os.environ["OPENAI_API_KEY"] = "sk-.."
    main()

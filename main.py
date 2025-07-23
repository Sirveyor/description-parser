"""
main.py

This script serves as the main entry point for the description parser application.
It initializes the parser, allows the user to select an input file, and processes it.
It also handles errors and displays messages using a graphical interface if necessary."""

from tkinter import messagebox

try:
    import description_parser

except ImportError:
    messagebox.showinfo("Failed to import description_parser. \
          Ensure it is available in the current directory.")
def main():
    """
    The main function serves as the entry point for the program.
    It calls the main function of the description_parser module,
    which is responsible for executing the primary functionality
    of the program.
    """
    description_parser.main()



if __name__ == "__main__":
    main()

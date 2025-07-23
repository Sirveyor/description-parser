
import tkinter as tk
from tkinter import ttk
import pandas as pd

class CSVEditor:
    """
    A simple CSV editor using Tkinter and Pandas.
    
    This class provides a graphical interface to view and edit CSV files.
    It used a Tkinter Treeview widget to dislplay the CSV data i a tabular format
    """
    def __init__(self, csv_file):
        """
        Initialize the CSVEditor with the spcified CSV file.
        
        Args:
            csv_file (str): Path to the CSV file to be loaded and edited.
        """
        self.csv_file = csv_file
        self.df = pd.read_csv(csv_file)  # Load the CSV file into a Pandas DataFrame
        self.root = tk.Tk()  # Create the main application window
        self.root.title("Description Editor") #  Set the title of the window

        # Create a Treeview widget to display the CSV data
        self.tree = ttk.Treeview(self.root, columns=list(self.df.columns), show='headings')
        self.tree.pack(expand=True, fill='both')  # Expand the Treeview to fill the window

        # Set up columns in the Treeview
        for col in self.df.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor='center')

        # Insert the CSV data into Treeview
        for index, row in self.df.iterrows():
            self.tree.insert("", "end", values=list(row))  # Insert each row of data

        # Add a button to save changes made to the CSV
        save_button = tk.Button(self.root, text="Save Changes", command=self.save_changes)
        save_button.pack()  # Pack the button into the window

        # Bind double-click event to allow editing of cells
        self.tree.bind('<Double-1>', self.on_double_click)

    def on_double_click(self, event):
        item = self.tree.selection()[0]
        column = self.tree.identify_column(event.x)
        column_index = int(column.replace('#', '')) - 1
        value = self.tree.item(item, 'values')[column_index]

        # Create an entry widget to edit the cell
        entry = tk.Entry(self.root)
        entry.insert(0, value)
        entry.place(x=event.x, y=event.y)
        entry.focus()

        def save_edit(event):
            new_value = entry.get()
            self.tree.set(item, column=column, value=new_value)
            entry.destroy()

        entry.bind('<Return>', save_edit)

    def save_changes(self):
        """
        save the changes made in the Treeview back to the CSV file.
        """
        # Update DataFrame with Treeview data
        for row_index, item in enumerate(self.tree.get_children()):
            row_values = self.tree.item(item, 'values')
            self.df.iloc[row_index] = row_values

        # Save DataFrame to CSV
        self.df.to_csv(self.csv_file, index=False)
        print("Changes saved to", self.csv_file)

    def run(self):
        self.root.mainloop()
        self.root.destroy()

if __name__ == "__main__":
    editor = CSVEditor("your_final_csv_file.csv")
    editor.run()
     # Close the Tkinter root window after editing
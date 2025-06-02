import tkinter as tk
from tkinter import messagebox, ttk
from reportlab.pdfgen import canvas

# ---------------------
# Story Templates
# ---------------------
STORIES = {
    "Zoo Adventure": {
        "template": (
            "Today I went to the zoo. I saw a(n) {adj1} {noun1} jumping up and down in its tree. "
            "It {verb1} {adverb1} through the large tunnel that led to its {adj2} {noun2}."
        ),
        "fields": {
            "adj1": "Adjective",
            "noun1": "Noun",
            "verb1": "Verb (past tense)",
            "adverb1": "Adverb",
            "adj2": "Another Adjective",
            "noun2": "Another Noun"
        }
    },
    "Alien Encounter": {
        "template": (
            "Last night I saw a(n) {adj1} light in the sky. I looked up and saw a {adj2} alien "
            "with {noun1} eyes. It landed its {noun2} right in front of me and said '{verb1}!' "
            "Then it {verb2} away into the night."
        ),
        "fields": {
            "adj1": "Adjective (for light)",
            "adj2": "Adjective (for alien)",
            "noun1": "Body Part (plural)",
            "noun2": "Vehicle",
            "verb1": "Exclamation",
            "verb2": "Verb (past tense)"
        }
    }
}

class MadLibsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mad Libs Generator")

        self.story_choice = tk.StringVar()
        self.entries = {}
        self.story = ""

        # Dropdown to select story
        dropdown_frame = tk.Frame(root)
        dropdown_frame.pack(pady=10)
        tk.Label(dropdown_frame, text="Choose a Story:", font=("Arial", 12)).pack(side=tk.LEFT, padx=5)

        self.story_menu = ttk.Combobox(dropdown_frame, textvariable=self.story_choice, state="readonly",
                                        values=list(STORIES.keys()), width=30)
        self.story_menu.pack(side=tk.LEFT)
        self.story_menu.bind("<<ComboboxSelected>>", self.build_form)

        # Frame to hold entry fields
        self.form_frame = tk.Frame(root)
        self.form_frame.pack(pady=10)

        # Buttons
        button_frame = tk.Frame(root)
        button_frame.pack(pady=10)
        tk.Button(button_frame, text="Generate Story", command=self.generate_story).grid(row=0, column=0, padx=10)
        tk.Button(button_frame, text="Download PDF", command=self.download_pdf).grid(row=0, column=1, padx=10)

        # Output Text Box
        self.output_text = tk.Text(root, height=12, width=80, wrap=tk.WORD)
        self.output_text.pack(pady=10)

    def build_form(self, event=None):
        for widget in self.form_frame.winfo_children():
            widget.destroy()

        self.entries.clear()
        story_key = self.story_choice.get()
        if not story_key:
            return

        fields = STORIES[story_key]["fields"]

        for key, label_text in fields.items():
            row = tk.Frame(self.form_frame)
            row.pack(fill="x", pady=3)

            label = tk.Label(row, text=label_text + ":", width=25, anchor='w', font=("Arial", 10))
            entry = tk.Entry(row, width=40)

            label.pack(side=tk.LEFT, padx=5)
            entry.pack(side=tk.LEFT)

            self.entries[key] = entry

    def generate_story(self):
        if not self.story_choice.get():
            messagebox.showerror("Missing Info", "Please select a story first.")
            return

        fields = STORIES[self.story_choice.get()]["fields"]
        filled = {key: self.entries[key].get().strip() for key in fields}

        if not all(filled.values()):
            messagebox.showerror("Missing Info", "Please fill in all fields.")
            return

        template = STORIES[self.story_choice.get()]["template"]
        self.story = template.format(**filled)
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(tk.END, self.story)

    def download_pdf(self):
        if not self.story:
            messagebox.showerror("No Story", "Generate a story first.")
            return

        filename = "madlibs_story.pdf"
        c = canvas.Canvas(filename)
        text_object = c.beginText(50, 800)
        text_object.setFont("Helvetica", 12)

        for line in self.story.split('\n'):
            text_object.textLine(line)

        c.drawText(text_object)
        c.save()
        messagebox.showinfo("Success", f"PDF saved as {filename}")

# Launch
if __name__ == "__main__":
    root = tk.Tk()
    app = MadLibsApp(root)
    root.mainloop()

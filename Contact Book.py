import tkinter as tk
from tkinter import messagebox, simpledialog
import json, os

# File to store contacts
CONTACTS_FILE = "contacts.json"

# Load contacts from file
def load_contacts():
    if os.path.exists(CONTACTS_FILE):
        with open(CONTACTS_FILE, "r") as f:
            return json.load(f)
    return []

# Save contacts to file
def save_contacts():
    with open(CONTACTS_FILE, "w") as f:
        json.dump(contacts, f, indent=4)

# Add new contact
def add_contact():
    name = simpledialog.askstring("Add Contact", "Enter Name:")
    phone = simpledialog.askstring("Add Contact", "Enter Phone Number:")
    email = simpledialog.askstring("Add Contact", "Enter Email:")
    address = simpledialog.askstring("Add Contact", "Enter Address:")
    
    if name and phone:
        contacts.append({"name": name, "phone": phone, "email": email, "address": address})
        save_contacts()
        render_contacts()
        messagebox.showinfo("Success", "Contact added successfully!")
    else:
        messagebox.showwarning("Input Error", "Name and Phone are required!")

# Update contact
def update_contact(contact):
    name = simpledialog.askstring("Update Contact", "Enter Name:", initialvalue=contact["name"])
    phone = simpledialog.askstring("Update Contact", "Enter Phone:", initialvalue=contact["phone"])
    email = simpledialog.askstring("Update Contact", "Enter Email:", initialvalue=contact["email"])
    address = simpledialog.askstring("Update Contact", "Enter Address:", initialvalue=contact["address"])
    
    if name and phone:
        contact.update({"name": name, "phone": phone, "email": email, "address": address})
        save_contacts()
        render_contacts()
        messagebox.showinfo("Success", "Contact updated successfully!")

# Delete contact
def delete_contact(contact):
    confirm = messagebox.askyesno("Delete Contact", f"Are you sure you want to delete {contact['name']}?")
    if confirm:
        contacts.remove(contact)
        save_contacts()
        render_contacts()
        messagebox.showinfo("Deleted", "Contact deleted successfully!")

# Search contacts
def search_contact():
    query = simpledialog.askstring("Search Contact", "Enter Name or Phone:")
    if query:
        filtered = [c for c in contacts if query.lower() in c["name"].lower() or query in c["phone"]]
        render_contacts(filtered)
    else:
        render_contacts()

# Clear and render contact cards
def render_contacts(filtered=None):
    for widget in contacts_frame.winfo_children():
        widget.destroy()
    
    display = filtered if filtered is not None else contacts
    colors = ["#1E90FF", "#00BFFF", "#4682B4", "#5F9EA0", "#4169E1", "#6495ED"]  # blue shades for initials
    for idx, contact in enumerate(display):
        card = tk.Frame(contacts_frame, bg="#E6F0FA", bd=2, relief="ridge")
        card.pack(fill="x", pady=10, padx=20, ipadx=5, ipady=5)

        # Profile icon (initials)
        initials = "".join([n[0] for n in contact["name"].split()][:2]).upper()
        icon_color = colors[idx % len(colors)]
        icon = tk.Label(card, text=initials, bg=icon_color, fg="white", font=("Helvetica", 16, "bold"), width=4, height=2)
        icon.pack(side="left", padx=10, pady=10)

        # Contact info
        info = tk.Frame(card, bg="#E6F0FA")
        info.pack(side="left", fill="x", expand=True)
        tk.Label(info, text=contact["name"], bg="#E6F0FA", fg="#0B3D91", font=("Helvetica", 14, "bold")).pack(anchor="w")
        tk.Label(info, text=contact["phone"], bg="#E6F0FA", fg="#1E3A8A", font=("Helvetica", 12)).pack(anchor="w")
        tk.Label(info, text=contact.get("email", ""), bg="#E6F0FA", fg="#415A77", font=("Helvetica", 10)).pack(anchor="w")
        tk.Label(info, text=contact.get("address", ""), bg="#E6F0FA", fg="#415A77", font=("Helvetica", 10)).pack(anchor="w")

        # Action buttons (Update/Delete)
        actions = tk.Frame(card, bg="#E6F0FA")
        actions.pack(side="right", padx=10, pady=10)
        tk.Button(actions, text="✏️ Update", bg="#0073E6", fg="white",
                  font=("Helvetica", 10, "bold"), width=10, relief="flat",
                  command=lambda c=contact: update_contact(c)).pack(pady=3)
        tk.Button(actions, text="🗑️ Delete", bg="#FF4500", fg="white",
                  font=("Helvetica", 10, "bold"), width=10, relief="flat",
                  command=lambda c=contact: delete_contact(c)).pack(pady=3)

# Main Window
root = tk.Tk()
root.title("📇 Contact Book")
root.geometry("700x750")
root.config(bg="#B0C4DE")  # light blue background

# Header
header = tk.Label(root, text="Contact Book", font=("Helvetica", 28, "bold"), fg="#0B3D91", bg="#B0C4DE")
header.pack(pady=20)

# Top Buttons
top_frame = tk.Frame(root, bg="#B0C4DE")
top_frame.pack(pady=10)
tk.Button(top_frame, text="➕ Add Contact", bg="#1E90FF", fg="white", font=("Helvetica", 12, "bold"), width=15, command=add_contact).pack(side="left", padx=10)
tk.Button(top_frame, text="🔍 Search Contact", bg="#00BFFF", fg="white", font=("Helvetica", 12, "bold"), width=15, command=search_contact).pack(side="left", padx=10)

# Main content frame (canvas + scrollbar)
main_frame = tk.Frame(root, bg="#B0C4DE")
main_frame.pack(fill="both", expand=True, padx=5, pady=5)

canvas = tk.Canvas(main_frame, bg="#B0C4DE", highlightthickness=0)
scrollbar = tk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
contacts_frame = tk.Frame(canvas, bg="#B0C4DE")

contacts_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

canvas.create_window((0, 0), window=contacts_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# Load contacts
contacts = load_contacts()
render_contacts()

# Footer
footer = tk.Label(root, text="✨ Designed by Kriti Sharma", font=("Helvetica", 10, "bold"), bg="#1E90FF", fg="white")
footer.pack(side="bottom", fill="x", pady=10)

root.mainloop()

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import json
import os

FICHIER_JSON = "tech_be.json"

def charger_techniciens():
    if os.path.exists(FICHIER_JSON):
        with open(FICHIER_JSON, "r", encoding="utf-8") as f:
            return json.load(f).get("tech_be", [])
    return []

def sauvegarder_techniciens(techs):
    with open(FICHIER_JSON, "w", encoding="utf-8") as f:
        json.dump({"tech_be": techs}, f, indent=2, ensure_ascii=False)

class GestionTechBEApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestion des techniciens BE")
        self.techniciens = charger_techniciens()
        self.selection_index = None

        self.setup_ui()

    def setup_ui(self):
        ttk.Label(self.root, text="Liste des techniciens BE", font=("Segoe UI", 16, "bold")).pack(pady=10)

        columns = ("Nom", "Prénom", "Email", "Téléphone", "Actif")
        self.tree = ttk.Treeview(self.root, columns=columns, show="headings", bootstyle="info")

        # Configuration des colonnes
        self.tree.heading("Nom", text="Nom", anchor="w")
        self.tree.heading("Prénom", text="Prénom", anchor="w")
        self.tree.heading("Email", text="Email", anchor="w")
        self.tree.heading("Téléphone", text="Téléphone", anchor="center")
        self.tree.heading("Actif", text="Actif", anchor="center")

        self.tree.column("Nom", width=160, anchor="w")
        self.tree.column("Prénom", width=160, anchor="w")
        self.tree.column("Email", width=320, anchor="w")
        self.tree.column("Téléphone", width=140, anchor="center")
        self.tree.column("Actif", width=80, anchor="center")

        self.tree.pack(padx=10, pady=10, fill="both", expand=True)
        self.tree.bind("<Double-1>", self.selectionner_technicien)

        style = ttk.Style()
        style.configure("Treeview", font=("Segoe UI", 11))
        style.configure("Treeview.Heading", font=("Segoe UI", 11, "bold"))

        # Formulaire
        form_frame = ttk.Frame(self.root)
        form_frame.pack(pady=10, padx=10, fill="x")

        labels = ["Nom", "Prénom", "Email", "Téléphone"]
        widths = [20, 20, 40, 20]
        self.entries = []

        for i, (label, width) in enumerate(zip(labels, widths)):
            ttk.Label(form_frame, text=label).grid(row=0, column=i, padx=5, sticky="w")
            entry = ttk.Entry(form_frame, width=width)
            entry.grid(row=1, column=i, padx=5, sticky="we")
            self.entries.append(entry)

        self.nom_entry, self.prenom_entry, self.email_entry, self.telephone_entry = self.entries

        self.actif_var = ttk.BooleanVar(value=True)
        ttk.Checkbutton(form_frame, text="Actif", variable=self.actif_var, bootstyle="success").grid(row=1, column=4, padx=10)

        self.btn_ajouter_modifier = ttk.Button(form_frame, text="Ajouter", command=self.ajouter_ou_modifier_technicien, bootstyle="primary")
        self.btn_ajouter_modifier.grid(row=1, column=5, padx=10)

        form_frame.columnconfigure((0, 1, 2, 3), weight=1)  # responsive columns

        self.actualiser_tableau()

    def actualiser_tableau(self):
        self.tree.delete(*self.tree.get_children())

        # Tri par nom (majuscules pour uniformiser)
        techniciens_tries = sorted(self.techniciens, key=lambda t: t["nom"].upper())

        for tech in techniciens_tries:
            nom_maj = tech["nom"].upper()
            actif_icon = "✓" if tech["actif"] else "✗"
            self.tree.insert(
                "", "end",
                values=(
                    nom_maj,
                    tech["prenom"],
                    tech["email"],
                    tech.get("telephone", ""),
                    actif_icon
                )
            )

    def ajouter_ou_modifier_technicien(self):
        nom = self.nom_entry.get().strip()
        prenom = self.prenom_entry.get().strip()
        email = self.email_entry.get().strip()
        telephone = self.telephone_entry.get().strip()
        actif = self.actif_var.get()

        if not nom or not prenom or not email:
            ttk.Messagebox.show_warning("Champs manquants", "Veuillez remplir tous les champs obligatoires.")
            return

        tech_data = {
            "nom": nom,
            "prenom": prenom,
            "email": email,
            "telephone": telephone,
            "actif": actif
        }

        if self.selection_index is not None:
            self.techniciens[self.selection_index] = tech_data
            self.selection_index = None
            self.btn_ajouter_modifier.config(text="Ajouter")
        else:
            self.techniciens.append(tech_data)

        self.vider_formulaire()
        self.actualiser_tableau()
        sauvegarder_techniciens(self.techniciens)

    def selectionner_technicien(self, event):
        item = self.tree.focus()
        if not item:
            return
        values = self.tree.item(item)["values"]
        for idx, tech in enumerate(self.techniciens):
            if tech["nom"].upper() == values[0] and tech["prenom"] == values[1] and tech["email"] == values[2]:
                self.selection_index = idx
                self.nom_entry.delete(0, "end")
                self.nom_entry.insert(0, tech["nom"])
                self.prenom_entry.delete(0, "end")
                self.prenom_entry.insert(0, tech["prenom"])
                self.email_entry.delete(0, "end")
                self.email_entry.insert(0, tech["email"])
                self.telephone_entry.delete(0, "end")
                self.telephone_entry.insert(0, tech.get("telephone", ""))
                self.actif_var.set(tech["actif"])
                self.btn_ajouter_modifier.config(text="Modifier")
                break

    def vider_formulaire(self):
        for entry in self.entries:
            entry.delete(0, "end")
        self.actif_var.set(True)
        self.selection_index = None
        self.btn_ajouter_modifier.config(text="Ajouter")

if __name__ == "__main__":
    app = ttk.Window("Techniciens BE", themename="flatly", size=(1080, 600), resizable=(True, True))
    app.iconbitmap("omexom.ico")
    GestionTechBEApp(app)
    app.mainloop()
import tkinter as tk
import os
import json

# Soubor pro ukládání skóre
SAVE_FILE = "save.json"

def load_data():
    """Načtení uložených dat ze souboru"""
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r") as file:
            return json.load(file)
    return {"score": 0, "buildings": {"Farm": 0, "Factory": 0, "Mine": 0}, "upgrades": {}}

def save_data():
    """Uložení dat do souboru"""
    with open(SAVE_FILE, "w") as file:
        json.dump({"score": score, "buildings": buildings, "upgrades": upgrades}, file)

def click():
    """Zvýšení skóre při kliknutí"""
    global score
    score += 1
    update_ui()
    save_data()

def passive_income():
    """Získávání bodů z budov"""
    global score
    for b in buildings:
        income = base_income[b] * (upgrades.get(b, 1))
        score += buildings[b] * income
    update_ui()
    save_data()
    root.after(1000, passive_income)

def buy_building(name, cost):
    """Koupě budovy (jen jednou)"""
    global score
    if score >= cost and buildings[name] == 0:
        score -= cost
        buildings[name] = 1
        buy_buttons[name].config(state=tk.DISABLED, bg="gray")
        update_ui()
        save_data()

def buy_upgrade(building):
    """Koupě vylepšení budovy (max level 10)"""
    global score
    current_level = upgrades.get(building, 1)
    if current_level < 10:
        upgrade_cost = upgrade_prices[building] * current_level
        if score >= upgrade_cost:
            score -= upgrade_cost
            upgrades[building] = current_level + 1
            update_ui()
            save_data()

def show_details(building):
    """Zobrazení detailů budovy"""
    detail_window = tk.Toplevel(root)
    detail_window.title(f"Detail {building}")
    level = upgrades.get(building, 1)
    income = base_income[building] * level
    tk.Label(detail_window, text=f"{building} - Level: {level}", font=("Arial", 14)).pack()
    tk.Label(detail_window, text=f"Příjem: {income} bodů/s", font=("Arial", 12)).pack()


def update_ui():
    """Aktualizace zobrazení skóre, budov a vylepšení"""
    label.config(text=f"Skóre: {score}")
    for b in buildings:
        income = base_income[b] * (upgrades.get(b, 1))
        level = upgrades.get(b, 1)
        building_labels[b].config(text=f"{b}: Level {level} (Příjem: {income} za sekundu)")
        if buildings[b] > 0:
            status_labels[b].config(text="Zakoupeno")
            buy_buttons[b].config(state=tk.DISABLED, bg="gray")
            if level < 10:
                upgrade_cost = upgrade_prices[b] * level
                upgrade_buttons[b].config(text=f"Vylepšit {b} ({upgrade_cost} bodů)")
                upgrade_buttons[b].pack()
            else:
                upgrade_buttons[b].pack_forget()
            detail_buttons[b].pack()
        else:
            status_labels[b].config(text="")
            upgrade_buttons[b].pack_forget()
            detail_buttons[b].pack_forget()

# Inicializace okna
root = tk.Tk()
root.title("Clicker Hra")
root.geometry("500x500")

frame_main = tk.Frame(root)
frame_main.pack(pady=20)

label = tk.Label(frame_main, text=f"Skóre: 0", font=("Arial", 20))
label.pack()

button = tk.Button(frame_main, text="Klikni!", font=("Arial", 24, "bold"), width=10, height=2, command=click)
button.pack(pady=10)



frame_buildings = tk.Frame(root)
frame_buildings.pack()

building_labels = {}
status_labels = {}
upgrade_buttons = {}
detail_buttons = {}
buy_buttons = {}

data = load_data()
score = data["score"]
buildings = data["buildings"]
upgrades = data.get("upgrades", {})

base_income = {"Farm": 1, "Factory": 5, "Mine": 10}
upgrade_prices = {"Farm": 20, "Factory": 100, "Mine": 500}

for name, cost in zip(["Farm", "Factory", "Mine"], [10, 50, 200]):
    frame = tk.Frame(frame_buildings, relief=tk.RIDGE, borderwidth=2)
    frame.pack(side=tk.LEFT, padx=10, pady=10)
    
    lbl = tk.Label(frame, text=f"{name}: Level {upgrades.get(name, 1)} (Příjem: {base_income[name]} za sekundu)", font=("Arial", 12))
    lbl.pack()
    building_labels[name] = lbl
    
    status_lbl = tk.Label(frame, text="")
    status_lbl.pack()
    status_labels[name] = status_lbl
    
    buy_buttons[name] = tk.Button(frame, text=f"Koupit {name} ({cost} bodů)", command=lambda n=name, c=cost: buy_building(n, c))
    buy_buttons[name].pack()
    
    upg_btn = tk.Button(frame, text=f"Vylepšit {name}", command=lambda n=name: buy_upgrade(n))
    upgrade_buttons[name] = upg_btn
    
    detail_btn = tk.Button(frame, text=f"Detail {name}", command=lambda n=name: show_details(n))
    detail_buttons[name] = detail_btn
    
    if buildings[name] > 0:
        status_lbl.config(text="Zakoupeno")
        buy_buttons[name].config(state=tk.DISABLED, bg="gray")
        if upgrades.get(name, 1) < 10:
            upg_btn.pack()
        else:
            upg_btn.pack_forget()
        detail_btn.pack()
    else:
        upg_btn.pack_forget()
        detail_btn.pack_forget()

# Spuštění pasivního příjmu
root.after(1000, passive_income)
root.mainloop()

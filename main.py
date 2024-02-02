import tkinter as tk
from tkinter import messagebox

class Plant:
	def __init__(self):
		self.growth_level = 0.0
		self.growth_rate = 0.0

	def update_growth(self):
		self.growth_level = round(self.growth_level + self.growth_rate, 1)

class Tooltip:
	def __init__(self, widget, text):
		self.widget = widget
		self.text = text
		self.tooltip = None
		self.widget.bind("<Enter>", self.show_tooltip)
		self.widget.bind("<Leave>", self.hide_tooltip)

	def show_tooltip(self, event):
		x, y, _, _ = self.widget.bbox("insert")
		x += self.widget.winfo_rootx() + 25
		y += self.widget.winfo_rooty() + 25

		self.tooltip = tk.Toplevel(self.widget)
		self.tooltip.wm_overrideredirect(True)
		self.tooltip.wm_geometry(f"+{x}+{y}")

		label = tk.Label(self.tooltip, text=self.text, background="#ffffe0", relief="solid", borderwidth=1)
		label.pack(ipadx=1)

		self.widget.bind("<Button-1>", self.hide_tooltip)

	def hide_tooltip(self, event=None):
		if self.tooltip:
			self.tooltip.destroy()
			self.tooltip = None

class PlantGameApp:
	def __init__(self, master):
		self.master = master
		self.master.title("Plant Clicker")
		self.master.attributes('-fullscreen', True)

		self.initial_state()

	def initial_state(self):
		self.plant = None
		self.water_button_price = 15
		self.fertilizer_button_price = 100
		self.prune_button_price = 600
		self.pesticide_button_price = 4000
		self.water_button_clicks = 0
		self.fertilizer_button_clicks = 0
		self.prune_button_clicks = 0
		self.pesticide_button_clicks = 0
		self.create_widgets()

	def create_widgets(self):
		self.create_plant_button()

	def create_plant_button(self):
		self.plant_button = tk.Button(self.master, text="Plant Your First Seed!", command=self.plant_seed, bg="#f0f0f0", fg="black", activebackground="#f0f0f0")
		self.plant_button.pack(expand=True, fill=tk.BOTH)
		self.center_window()

	def center_window(self):
		width = self.master.winfo_screenwidth() // 2
		height = self.master.winfo_screenheight() // 2
		x = (self.master.winfo_screenwidth() - width) // 2
		y = (self.master.winfo_screenheight() - height) // 2
		self.master.geometry(f"{width}x{height}+{x}+{y}")

	def plant_seed(self):
		self.plant = Plant()

		for widget in self.master.winfo_children():
			widget.destroy()

		self.create_grow_button()
		self.create_water_button()
		self.create_fertilizer_button()
		self.create_prune_button()
		self.create_pesticide_button()
		self.create_labels()
		self.create_restart_button()
		self.update_growth_periodically()

	def create_grow_button(self):
		self.grow_button = tk.Button(self.master, text="Grow (+1 growth level)", command=self.grow_plant, bg="#cccccc", fg="black")
		self.grow_button.pack(expand=True, fill=tk.BOTH)
		Tooltip(self.grow_button, "Increases growth level by 1.0")

	def create_water_button(self):
		self.water_button = tk.Button(self.master, text=f"Water (-{self.water_button_price} growth levels)", command=self.water_plant, bg="#bbbbbb", fg="black")
		self.water_button.pack(expand=True, fill=tk.BOTH)
		Tooltip(self.water_button, f"Increases growth rate by 0.1\nBought: {self.water_button_clicks}\nTotal Effect: {round(0.1 * self.water_button_clicks, 1)}")

	def create_fertilizer_button(self):
		self.fertilizer_button = tk.Button(self.master, text=f"Add Fertilizer (-{self.fertilizer_button_price} growth levels)", command=self.add_fertilizer, bg="#aaaaaa", fg="black")
		self.fertilizer_button.pack(expand=True, fill=tk.BOTH)
		Tooltip(self.fertilizer_button, f"Increases growth rate by 0.5\nBought: {self.fertilizer_button_clicks}\nTotal Effect: {round(0.5 * self.fertilizer_button_clicks, 1)}")

	def create_prune_button(self):
		self.prune_button = tk.Button(self.master, text=f"Prune (-{self.prune_button_price} growth levels)", command=self.prune_plant, bg="#999999", fg="black")
		self.prune_button.pack(expand=True, fill=tk.BOTH)
		Tooltip(self.prune_button, f"Increases growth rate by 5.0\nBought: {self.prune_button_clicks}\nTotal Effect: {round(5.0 * self.prune_button_clicks, 1)}")

	def create_pesticide_button(self):
		self.pesticide_button = tk.Button(self.master, text=f"Pesticide (-{self.pesticide_button_price} growth levels)", command=self.apply_pesticide, bg="#888888", fg="black")
		self.pesticide_button.pack(expand=True, fill=tk.BOTH)
		Tooltip(self.pesticide_button, f"Increases growth rate by 12.0\nBought: {self.pesticide_button_clicks}\nTotal Effect: {round(12.0 * self.pesticide_button_clicks, 1)}")

	def create_labels(self):
		self.growth_level_label = tk.Label(self.master, text=f"Growth Level: {self.plant.growth_level}", bg="#000000", fg="white")
		self.growth_level_label.pack(expand=True, fill=tk.BOTH)

		self.growth_rate_label = tk.Label(self.master, text=f"Growth Rate: {self.plant.growth_rate}", bg="#000000", fg="white")
		self.growth_rate_label.pack(expand=True, fill=tk.BOTH)

	def create_restart_button(self):
		self.restart_button = tk.Button(self.master, text="Restart", command=self.confirm_restart, bg="red", fg="white")
		self.restart_button.pack(expand=True, fill=tk.BOTH)

	def confirm_restart(self):
		confirm = messagebox.askyesno("Confirm Restart", "Are you sure you want to restart the game?")
		if confirm:
			self.restart_game()

	def restart_game(self):
		self.master.destroy()
		root = tk.Tk()
		app = PlantGameApp(root)
		root.mainloop()

	def grow_plant(self):
		self.plant.growth_level = round(self.plant.growth_level + 1.0, 1)
		self.update_display()

	def water_plant(self):
		if self.plant.growth_level >= self.water_button_price:
			self.plant.growth_level = round(self.plant.growth_level - self.water_button_price, 1)
			self.plant.growth_rate = round(self.plant.growth_rate + 0.1, 1)
			self.water_button_price = round(self.water_button_price * 1.15)
			self.water_button_clicks += 1
			self.water_button.config(text=f"Water (-{self.water_button_price} growth levels)")
			Tooltip(self.water_button, f"Increases growth rate by 0.1\nBought: {self.water_button_clicks}\nTotal Effect: {round(0.1 * self.water_button_clicks, 1)}")
			self.update_display()
		else:
			messagebox.showinfo("Insufficient Growth Levels", "You don't have enough growth levels to water the plant.")

	def add_fertilizer(self):
		if self.plant.growth_level >= self.fertilizer_button_price:
			self.plant.growth_level = round(self.plant.growth_level - self.fertilizer_button_price, 1)
			self.plant.growth_rate = round(self.plant.growth_rate + 0.5, 1)
			self.fertilizer_button_price = round(self.fertilizer_button_price * 1.15)
			self.fertilizer_button_clicks += 1
			self.fertilizer_button.config(text=f"Add Fertilizer (-{self.fertilizer_button_price} growth levels)")
			Tooltip(self.fertilizer_button, f"Increases growth rate by 0.5\nBought: {self.fertilizer_button_clicks}\nTotal Effect: {round(0.5 * self.fertilizer_button_clicks, 1)}")
			self.update_display()
		else:
			messagebox.showinfo("Insufficient Growth Levels", "You don't have enough growth levels to add fertilizer.")

	def prune_plant(self):
		if self.plant.growth_level >= self.prune_button_price:
			self.plant.growth_level = round(self.plant.growth_level - self.prune_button_price, 1)
			self.plant.growth_rate = round(self.plant.growth_rate + 5.0, 1)
			self.prune_button_price = round(self.prune_button_price * 1.15)
			self.prune_button_clicks += 1
			self.prune_button.config(text=f"Prune (-{self.prune_button_price} growth levels)")
			Tooltip(self.prune_button, f"Increases growth rate by 5.0\nBought: {self.prune_button_clicks}\nTotal Effect: {round(5.0 * self.prune_button_clicks, 1)}")
			self.update_display()
		else:
			messagebox.showinfo("Insufficient Growth Levels", "You don't have enough growth levels to prune the plant.")

	def apply_pesticide(self):
		if self.plant.growth_level >= self.pesticide_button_price:
			self.plant.growth_level = round(self.plant.growth_level - self.pesticide_button_price, 1)
			self.plant.growth_rate = round(self.plant.growth_rate + 12.0, 1)
			self.pesticide_button_price = round(self.pesticide_button_price * 1.15)
			self.pesticide_button_clicks += 1
			self.pesticide_button.config(text=f"Pesticide (-{self.pesticide_button_price} growth levels)")
			Tooltip(self.pesticide_button, f"Increases growth rate by 12.0\nBought: {self.pesticide_button_clicks}\nTotal Effect: {round(12.0 * self.pesticide_button_clicks, 1)}")
			self.update_display()
		else:
			messagebox.showinfo("Insufficient Growth Levels", "You don't have enough growth levels to apply pesticide.")
	
	def update_growth_periodically(self):
		self.update_display()
		self.master.after(1000, self.update_growth_periodically)

	def update_display(self):
		self.plant.update_growth()
		self.growth_level_label.config(text=f"Growth Level: {self.plant.growth_level}")
		self.growth_rate_label.config(text=f"Growth Rate: {self.plant.growth_rate}")

if __name__ == "__main__":
	root = tk.Tk()
	app = PlantGameApp(root)
	root.mainloop()
from customtkinter import *
from tkinter import messagebox, END
from PIL import Image
from datetime import datetime
import json
import os
import random

set_appearance_mode('dark')
set_default_color_theme('theme.json')

file_path = 'data.json'
current_user = None
current_data = None
colors = ['#a0c8d6', '#263f4f']
colors2 = ['#b4d9e7', '#1e3a46']
colors3 = ['#2C4F7C', '#E1F2F6']
# Parent Class for Frames
class ParentFrame(CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller # to reference the main app class as a variable
        self.grid_rowconfigure((0,1,2,3,4,5,6), weight=1, uniform='a')
        self.grid_columnconfigure(0, weight=1, uniform='a')

        self.__clear_widgets = [] # private attribute

    def append_widgets(self, widget_list):
        self.__clear_widgets = widget_list # add widgets to private attribute list

    def on_display(self):
        for w in self.__clear_widgets: # reset all feedback message, entry fields, scrollableframe
            if isinstance(w, CTkLabel): w.configure(text='')
            elif isinstance(w, CTkEntry): w.delete(0, END)
            elif isinstance(w, CTkScrollableFrame): w._parent_canvas.yview_moveto(0)
            elif isinstance(w, CTkOptionMenu): w.set(value='')
        self.tkraise()

    def exit_app(self): # for exit app (login page, signup page)
        confirm = messagebox.askyesno(title='Confirmation', message='Are you sure you want to exit the application?')
        if confirm:
            self.controller.destroy()

    def load_data(self): # load data from 'data.json'
        if not os.path.exists(file_path):
            with open(file_path, 'w') as f:
                json.dump({}, f, indent=4)
        with open(file_path, 'r') as f:
            return json.load(f)
        
    def save_data(self, data): # save data into 'data.json'
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=4)

    def check_empty(self, widget1, widget2, text): # check for empty user/pass for feedback
        if widget1.get() == '':
            widget2.configure(text=f'{text} cannot be empty.')
        else:
            widget2.configure(text='')

# Login Menu
class LoginMenu(ParentFrame):
    def __init__(self, master, controller):
        super().__init__(master, controller)

        img = CTkImage(dark_image=Image.open("neatlylogo.png"), size=(250, 250))
        self.frame = CTkFrame(self, width=450, height=650, corner_radius=30)
        self.frame.grid(row=0, column=0, rowspan=7)
        self.logo = CTkLabel(self, image=img, text='', bg_color=colors)
        self.logo.grid(row=0, column=0, sticky='n', rowspan=2, pady=(50, 0))

        self.header = CTkLabel(self, text='Account Login', font=controller.header_font, bg_color=colors)
        self.header.grid(row=1, column=0, sticky='s')
        self.label1 = CTkLabel(self, text='Username *', bg_color=colors)
        self.label1.grid(row=2, column=0, sticky='n', padx=(0, 60), pady=(20, 0))
        self.entry1 = CTkEntry(self, height=32, placeholder_text='Username', bg_color=colors)
        self.entry1.grid(row=2, column=0, pady=(25, 0))
        self.entry1.bind(sequence='<KeyRelease>', command=lambda event:self.check_empty(self.entry1, self.feedback1, 'Username'))
        self.entry1.bind(sequence='<FocusOut>', command=lambda event:self.check_empty(self.entry1, self.feedback1, 'Username'))
        self.feedback1 = CTkLabel(self, text='', text_color='orangered',bg_color=colors)
        self.feedback1.grid(row=2, column=0, rowspan=2)
        
        self.label2 = CTkLabel(self, text='Password *', bg_color=colors)
        self.label2.grid(row=3, column=0, padx=(0, 60), pady=(0, 30))
        self.entry2 = CTkEntry(self, height=32, placeholder_text='Password', show='*', bg_color=colors)
        self.entry2.grid(row=3, column=0, sticky='s', pady=(0, 20))
        self.entry2.bind(sequence='<KeyRelease>', command=lambda event:self.check_empty(self.entry2, self.feedback2, 'Password'))
        self.entry2.bind(sequence='<FocusOut>', command=lambda event:self.check_empty(self.entry2, self.feedback2, 'Password'))
        self.feedback2 = CTkLabel(self, text='', text_color='orangered', bg_color=colors)
        self.feedback2.grid(row=3, column=0, sticky='s', pady=(75, 0))

        self.button = CTkButton(self, width=160, height=32, text='Login Account', command=self.trylogin,
                                 font=controller.subheader_font, bg_color=colors)
        self.button.grid(row=4, column=0)
        self.signup = CTkButton(self, height=24, text='Don\'t have an account? Sign up', command=lambda:controller.show_frame(SignupMenu),
                                 fg_color=colors, bg_color=colors, hover=False, font=controller.underlined)
        self.signup.grid(row=4, column=0, sticky='s', pady=(10, 0))
        self.feedback3 = CTkLabel(self, text='', text_color='orangered', bg_color=colors)
        self.feedback3.grid(row=5, column=0, sticky='n')

        self.exit = CTkButton(self, width=160, height=30, text='Exit Application', command=self.exit_app,
                               font=controller.subheader_font, bg_color=colors)
        self.exit.grid(row=5, column=0, sticky='s')

        self.append_widgets([self.entry1, self.entry2, self.feedback1, self.feedback2, self.feedback3])

    def trylogin(self):
        username = self.entry1.get().strip()
        password = self.entry2.get().strip()
        
        rdata = self.load_data() # get data from file to iterate through
        if username in rdata and rdata[username]['password'] == password:
            # save current user and current data as variables
            loginSuccess = True
            global current_user
            current_user = username
            global current_data
            current_data = rdata[username]
            loginSuccess = True
        else:
            loginSuccess = False

        if loginSuccess:
            self.controller.show_frame(MainMenu)
            
        else:
            if username == '' or password == '':
                self.feedback3.configure(text='Please enter your username and password')
            else:
                self.feedback3.configure(text='Incorrect username or password')

# Signup Page
class SignupMenu(ParentFrame):
    def __init__(self, master, controller):
        super().__init__(master,controller)

        img = CTkImage(dark_image=Image.open("neatlylogo.png"), size=(250, 250))
        self.frame = CTkFrame(self, width=450, height=650, corner_radius=30)
        self.frame.grid(row=0, column=0, rowspan=7)
        self.logo = CTkLabel(self, image=img, text='', bg_color=colors)
        self.logo.grid(row=0, column=0, sticky='n', rowspan=2, pady=(50, 0))

        self.header = CTkLabel(self, text='Account Sign Up', font=controller.header_font, bg_color=colors)
        self.header.grid(row=1, column=0)

        self.label1 = CTkLabel(self, text='Username *', bg_color=colors)
        self.label1.grid(row=1, column=0, sticky='s', padx=(0, 60))
        self.entry1 = CTkEntry(self, height=32, placeholder_text='Username', bg_color=colors)
        self.entry1.grid(row=2, column=0, sticky='n')
        self.entry1.bind(sequence='<KeyRelease>', command=lambda event:self.check_empty(self.entry1, self.feedback1, 'Username'))
        self.entry1.bind(sequence='<FocusOut>', command=lambda event:self.check_empty(self.entry1, self.feedback1, 'Username'))
        self.feedback1 = CTkLabel(self, text='', text_color='orangered', bg_color=colors)
        self.feedback1.grid(row=2, column=0, pady=(15, 0))

        self.label2 = CTkLabel(self, text='Password *', bg_color=colors)
        self.label2.grid(row=2, column=0, sticky='s', padx=(0, 60))
        self.entry2 = CTkEntry(self, height=32, placeholder_text='Password', show='*', bg_color=colors)
        self.entry2.grid(row=3, column=0, sticky='n')
        self.entry2.bind(sequence='<KeyRelease>', command=lambda event:self.check_empty(self.entry2, self.feedback2, 'Password'))
        self.entry2.bind(sequence='<FocusOut>', command=lambda event:self.check_empty(self.entry2, self.feedback2, 'Password'))
        self.feedback2 = CTkLabel(self, text='', text_color='orangered', bg_color=colors)
        self.feedback2.grid(row=3, column=0, pady=(15, 0))

        self.label3 = CTkLabel(self, text='Confirm Password *', bg_color=colors)
        self.label3.grid(row=3, column=0, sticky='s')
        self.entry3 = CTkEntry(self, height=32, placeholder_text='Confirm Password', show='*', bg_color=colors)
        self.entry3.grid(row=4, column=0, sticky='n')

        self.button = CTkButton(self, width=160, height=32, text="Sign Up", command=self.trysignup,
                                 font=controller.subheader_font, bg_color=colors)
        self.button.grid(row=4, column=0, pady=(45, 0))

        self.back = CTkButton(self, height=24, text='Already have an account? Login', command=lambda:controller.show_frame(LoginMenu),
                               font=controller.underlined, fg_color=colors, bg_color=colors, hover=False)
        self.back.grid(row=5, column=0, sticky='n')

        self.feedback3 = CTkLabel(self, text='', bg_color=colors)
        self.feedback3.grid(row=5, column=0, pady=(5, 0))
        
        self.exit = CTkButton(self, width=160, height=30, text='Exit Application', command=self.exit_app,
                               font=controller.subheader_font, bg_color=colors)
        self.exit.grid(row=5, column=0, sticky='s')
        
        self.append_widgets([self.entry1, self.entry2, self.entry3, self.feedback1, self.feedback2, self.feedback3])

    def trysignup(self):
        username = self.entry1.get().strip()
        password = self.entry2.get().strip()
        conpassword = self.entry3.get().strip()
            
        if username == '' and password == '':
            self.feedback3.configure(text='Please enter username and password!', text_color='orangered')
            return
        
        rdata = self.load_data()
        for k in rdata:
            if username.lower() == k.lower():
                self.feedback3.configure(text='Username already exists! Please try a different username.', text_color='orangered')
                return
            
        if password != conpassword or password == '':
                self.feedback3.configure(text="Password and confirm password does not match. Please try again!", text_color='orangered')

        elif password == conpassword and username != '' and password != '': 
                self.feedback3.configure(text=f"Sign-up successful, Welcome {username}!", text_color='cyan')
                rdata[username] = {
                    'password': password,
                    'grocery_list': {},
                    'income': [],
                    'expenses': [],
                    'overall_budget': 0,
                    'budgets': {
                        'Food & Drinks': 0,
                        'Entertainment': 0,
                        'Shops': 0,
                        'Rent': 0,
                        'Utility': 0,
                        'Others': 0
                    },
                    'meal_plan' : ''
                }

                self.save_data(rdata)

# Main Menu (Lead to Grocery List Manager, Budget Tracker, Meal Planner)
class MainMenu(ParentFrame):
    def __init__(self, master, controller):
        super().__init__(master, controller)

        self.frame = CTkFrame(self, width=750, height=250, corner_radius=30)
        self.frame.grid(row=2, column=0, rowspan=3, ipady=60)
        
        img_main = CTkImage(dark_image=Image.open("neatlylogo.png"), size=(300, 300))
        img_grocery = CTkImage(dark_image=Image.open("grocerylogo.png"), size=(200, 200))
        img_budget = CTkImage(dark_image=Image.open("budgetlogo.png"), size=(200, 200))
        img_meal = CTkImage(dark_image=Image.open("meallogo.png"), size=(200, 200))

        self.logo = CTkLabel(self, image=img_main, text='')
        self.logo.grid(row=0, column=0, sticky='n', rowspan=2)

        self.logo2 = CTkLabel(self, image=img_grocery, text='', bg_color=colors)
        self.logo2.grid(row=2, column=0,rowspan=2, sticky='sw', padx=(35,0))
        self.logo3 = CTkLabel(self, image=img_budget, text='', bg_color=colors)
        self.logo3.grid(row=2, column=0,rowspan=2, sticky='s',pady=(0,0))
        self.logo4 = CTkLabel(self, image=img_meal, text='', bg_color=colors)
        self.logo4.grid(row=2, column=0,rowspan=2, sticky='se', padx=(0,35))

        self.label = CTkLabel(self, text='Selection Menu', font=controller.header_font,fg_color=colors2)
        self.label.grid(row=1, column=0, padx=20)
        
        self.decide = CTkButton(self, text="Grocery List Manager", command=lambda:controller.show_frame(GroceryMenu),
                                 font=controller.bold, bg_color=colors)
        self.decide.grid(row=4, column=0, sticky='nw', padx=(55,0), pady=(20, 0))
        self.decide2 = CTkButton(self, text="Budget Tracker", command=lambda:controller.show_frame(BudgetMenu),
                                 font=controller.bold, bg_color=colors)
        self.decide2.grid(row=4, column=0, sticky='n', pady=(20, 0))
        self.decide3 = CTkButton(self, text="Meal Planner", command=lambda:controller.show_frame(MealMenu),
                                 font=controller.bold, bg_color=colors)
        self.decide3.grid(row=4, column=0, sticky='ne',padx=(0,60), pady=(20, 0))

        self.decide4 = CTkButton(self, height=32, width=160, text="Log Out", command=lambda:controller.show_frame(LoginMenu),
                                 font=controller.subheader_font, corner_radius=30)
        self.decide4.grid(row=5, column=0)

    def on_display(self):
        super().on_display()
        self.label.configure(text=f'Welcome, {current_user}!\nPlan ahead with our app\'s features!')

class GroceryMenu(ParentFrame):
    def __init__(self, master, controller):
        super().__init__(master, controller)
        self.grid_rowconfigure((0,1,2,3,4,5,6,7,8), weight = 1)
        self.grid_columnconfigure((0), weight = 1)

        #items for Grocery Menu
        self.category_items = {
            "Dairy": ["Milk", "Butter", "Cheese", "Yogurt", "Cream", "Ice Cream"],
            "Meat": ["Beef", "Pork", "Lamb", "Bacon", "Sausage"],
            "Poultry": ["Chicken", "Turkey", "Duck", "Chicken Wings"],
            "Seafood": ["Fish", "Shrimp", "Crab", "Salmon", "Tuna"],
            "Eggs": ["Eggs", "Quail Eggs", "Duck Eggs"],
            "Vegetables": ["Tomatoes", "Potatoes", "Onions", "Carrots", "Lettuce", "Broccoli", "Spinach"],
            "Fruits": ["Apples", "Bananas", "Oranges", "Grapes", "Strawberries", "Watermelon"],
            "Grains": ["Rice", "Wheat", "Quinoa", "Oats", "Barley"],
            "Cereals": ["Cereal", "Cornflakes", "Granola", "Muesli"],
            "Baked Goods": ["Bread", "Bagels", "Croissants", "Muffins", "Donuts"],
            "Legumes": ["Beans", "Lentils", "Chickpeas", "Peas"],
            "Nuts": ["Almonds", "Walnuts", "Cashews", "Peanuts"],
            "Seeds": ["Sunflower Seeds", "Chia Seeds", "Flax Seeds"],
            "Snacks": ["Chips", "Crackers", "Pretzels", "Popcorn"],
            "Sweets": ["Chocolate", "Candy", "Cookies", "Cake"],
            "Fats & Oils": ["Oil", "Olive Oil", "Coconut Oil", "Butter"],
            "Herbs": ["Basil", "Oregano", "Thyme", "Rosemary"],
            "Spices": ["Salt", "Pepper", "Cinnamon", "Paprika"],
            "Condiments": ["Ketchup", "Mustard", "Mayonnaise", "Soy Sauce"],
            "Sauces": ["Tomato Sauce", "BBQ Sauce", "Hot Sauce", "Pasta Sauce"],
            "Beverages": ["Coffee", "Tea", "Juice", "Soda", "Water"],
            "Frozen Foods": ["Frozen Vegetables", "Frozen Pizza", "Ice Cream", "Frozen Meals"],
            "Canned Foods": ["Canned Beans", "Canned Soup", "Canned Tuna", "Canned Vegetables"],
            "Packaged Foods": ["Instant Noodles", "Pasta", "Crackers", "Cereal"],
            "Ready-to-Eat": ["Sandwiches", "Salads", "Deli Meats", "Prepared Meals"],
            "Others": ["Sugar", "Flour", "Baking Powder", "Vanilla Extract"]
        }

        self.label = CTkLabel(self, text="Grocery Management System", font=controller.header_font)
        self.label.grid(row=0, column=0, sticky="n", pady=30)

        self.tabs = CTkTabview(self, corner_radius=30)
        self.tabs.grid(row=0, column=0, rowspan=7, padx=15, pady=60, sticky='nsew')

        # Category Tab
        self.tabs.add('Category')
        self.category = self.tabs.tab('Category')
        self.category.grid_rowconfigure((0,1,2,3,4,5,6), weight=1, uniform='a')
        self.category.grid_columnconfigure(0, weight=1, uniform='a')

        # Overview Tab
        self.tabs.add('Inventory')
        self.inventory = self.tabs.tab('Inventory')
        self.inventory.grid_rowconfigure((0,1,2,3,4,5,6), weight=1, uniform='a')
        self.inventory.grid_columnconfigure(0, weight=1, uniform='a')

        #Main Tab
        self.add_label = CTkLabel(self.category, text='Additional Category/Items Add on', font=controller.header_font)
        self.add_label.grid(row=0, column=0, sticky='n')
        self.add_label2 = CTkFrame(self.category, width=300, height=2, fg_color='white')
        self.add_label2.grid(row=0, column=0, pady=(30, 0), sticky='n')

        #Category Dropdown
        self.cat_label_items = CTkLabel(self.category, text='Category : ')
        self.cat_label_items.grid(row=0, column=0, padx=(0, 188), pady=(30, 0), sticky='s')
        self.cat_dropdown_items = CTkOptionMenu(self.category, values=list(self.category_items.keys()), command=self.update_items_dropdown)
        self.cat_dropdown_items.set("Select a Category")
        self.cat_dropdown_items.grid(row=0, column=0, padx=(80, 0), pady=(47.5, 0), ipadx=20, sticky='s')

        #item dropdown (only available after the user have selected an item)
        self.items_label = CTkLabel(self.category, text='Item : ')
        self.items_label.grid(row=1, column=0, padx=(0, 160), pady=(10, 0), sticky='n')
        self.items_dropdown = CTkComboBox(self.category, values=[])
        self.items_dropdown.set("Select Category First")
        self.items_dropdown.grid(row=1, column=0, padx=(80, 0), pady=(10, 0), ipadx=20, sticky='n')

        self.qty_label = CTkLabel(self.category, text='Quantity : ')
        self.qty_label.grid(row=1, column=0,padx=(0,188), pady=(45,0), sticky="")
        self.qty_entry_items = CTkEntry(self.category, placeholder_text="E.g. 2")
        self.qty_entry_items.grid(row=1, column=0, padx=(40,0), pady=(45,0), sticky="s")
        self.additem_button = CTkButton(self.category, text='Add Items', command=self.add_items, font=controller.subheader_font)
        self.additem_button.grid(row=2, column=0, pady=(15, 0),padx=(0,150), rowspan=2, sticky='n')
        self.removeitem_button = CTkButton(self.category, text="Remove Items", command=self.remove_items, font=controller.subheader_font)
        self.removeitem_button.grid(row=2, column=0, pady=(15,0), padx=(150,0), rowspan=2, sticky='n')
        self.item_feedback = CTkLabel(self.category, text='')
        self.item_feedback.grid(row=2, column=0,pady=(50,0))

        self.list_frame = CTkScrollableFrame(self.category, fg_color=colors2)
        self.list_frame.grid(row=3, column=0, rowspan=3, sticky="nsew")
        self.columns = ['Item Name', 'Category', 'Quantity', 'Delete']
        for col, text in enumerate(self.columns):
            self.label = CTkLabel(self.list_frame, text=text, fg_color=colors, corner_radius=5)
            self.label.grid(row=0, column=col, padx=10, pady=5, sticky='nsew')
            self.list_frame.grid_columnconfigure(col, weight=1)

        #inventory tab# 
        #title for inventory
        self.add_label = CTkLabel(self.inventory, text='Inventory Viewer', font=controller.header_font)
        self.add_label.grid(row=0, column=0, sticky='n')
        self.add_label2 = CTkFrame(self.inventory, width=300, height=2, fg_color='white')
        self.add_label2.grid(row=0, column=0, pady=(30, 0), sticky='n')

        self.filter_label = CTkLabel(self.inventory, text="Filter by Category:", font=controller.header_font)
        self.filter_label.grid(row=0, column=0, pady=(40,0))

        # Dropdown with All (Display all / by category)
        self.filter_dropdown = CTkComboBox(self.inventory,values=["All"] + list(self.category_items.keys()),command=self.filter_inventory)
        self.filter_dropdown.set("All")
        self.filter_dropdown.grid(row=1, column=0, pady=(0,0), ipadx=20)

        self.inventory_frame = CTkScrollableFrame(self.inventory, fg_color=colors2)
        self.inventory_frame.grid(row=3, column=0, rowspan=3, sticky="nsew", padx=10, pady=20)
        self.columns = ['Item Name', 'Category', 'Quantity', 'Delete']
        for col, text in enumerate(self.columns):
            self.label = CTkLabel(self.inventory_frame, text=text, fg_color=colors, corner_radius=5)
            self.label.grid(row=0, column=col, padx=10, pady=5, sticky='nsew')
            self.inventory_frame.grid_columnconfigure(col, weight=1)

        self.selection_menu = CTkButton(self, text="Back to Main Menu", command=lambda:controller.show_frame(MainMenu),
                                        font=controller.subheader_font, height=45)
        self.selection_menu.grid(row=6, column=0)

        self.append_widgets([self.item_feedback, self.qty_entry_items, self.inventory_frame])

    def filter_inventory(self, category):
     # Clear old rows (except header, row 0)
        for widget in self.inventory_frame.winfo_children():
            if int(widget.grid_info()["row"]) != 0:
                widget.destroy()

        row = 1 # start at row = 1 because row = 0 is already taken by header

        for item, info in current_data["grocery_list"].items():

            # Category filter logic
            if category != "All" and info["category"] != category:
                continue

            # Item Name
            CTkLabel(self.inventory_frame, text=item).grid(
                row=row, column=0, padx=10, pady=5)

            # Category
            CTkLabel(self.inventory_frame, text=info["category"]).grid(
                row=row, column=1, padx=10, pady=5)

            # Quantity
            CTkLabel(self.inventory_frame, text=info["quantity"]).grid(
                row=row, column=2, padx=10, pady=5)

            # Delete Button
            delete_btn = CTkButton(
                self.inventory_frame,
                text="Delete",
                width=60,
                fg_color="#B33939",
                hover_color="#E55039",
                command=lambda item=item: self.delete_items(item)
            )
            delete_btn.grid(row=row, column=3, padx=10, pady=5)

            row += 1

        # If nothing found
        if row == 1:
            CTkLabel(self.inventory_frame, text="No items in this category.",
                    text_color="orange").grid(row=row, column=0, pady=10)

    #function to update tje scolable dropdown bar
    def update_items_dropdown(self, selected_category):
        if selected_category in self.category_items:
            items = self.category_items[selected_category]
            self.items_dropdown.configure(values=items)
            self.items_dropdown.set("")
        else:
            self.items_dropdown.configure(values=[])
            self.items_dropdown.set("No items available")

    #add quantity of the item from the specific item from grocery list
    def add_items(self):
        category = self.cat_dropdown_items.get().strip()
        item = self.items_dropdown.get().strip()
        qty = self.qty_entry_items.get().strip()
        
        if category == "Select a Category" or item == "Select Category First" or qty =="" or item =="" or category=="" or qty==0:
            self.item_feedback.configure(text="Please select category, item and key-in a quantity.", text_color="orangered")
            return
        
        # validate if quantity is a number
        if not qty.isdigit():
            self.item_feedback.configure(text="Quantity must be a number", text_color="orangered")
            return
        elif qty==0 or qty=="":
            self.item_feedback.configure(text="Quantity must greater than 0 ", text_color="orangered")
            return

        # to make sure quantity is an integer
        qty = int(qty)

        # add item into grocery list 
        if item not in current_data["grocery_list"]:
            current_data["grocery_list"][item] = {
                "category": category,
                "quantity": qty
            }
        else:
            current_data["grocery_list"][item]["quantity"] += qty


        # write new updated data into file
        data = self.load_data()

        # write the new data into the data file
        data[current_user]["grocery_list"] = current_data["grocery_list"]
        
        self.save_data(data)

        self.item_feedback.configure(text="Item added!", text_color="cyan")

        self.display_items()
        self.qty_entry_items.delete(0, END)

        self.filter_inventory(self.filter_dropdown.get())

    # remove quantity of the item from the specific item from grocery list
    def remove_items(self):
        category = self.cat_dropdown_items.get().strip()
        item = self.items_dropdown.get().strip()
        qty = self.qty_entry_items.get().strip()

        # check if the item item selected is in the data.json file or not
        if item not in current_data["grocery_list"]:
            self.item_feedback.configure(text="Item not found in list.", text_color="orangered")
            return
        
        # check if qty is a digit(number)
        if not qty.isdigit():
            self.item_feedback.configure(text="Quantity must be a number.", text_color="orangered")
            return

        # check if the qty is an interger
        qty = int(qty)

        # current quantity = qunantity retrieved from the data file
        current_qty = current_data["grocery_list"][item]["quantity"]

        if qty > current_qty:
            self.item_feedback.configure(text=f"Cannot deduct {qty}. Only {current_qty} available.",text_color="orangered"
            )
            return

        # update the new quantity
        new_qty = current_qty - qty

        if new_qty <= 0:
            del current_data["grocery_list"][item]
        else:
            current_data["grocery_list"][item]["quantity"] = new_qty

        # save the new data back into the data.json file
        data = self.load_data()

        data[current_user]["grocery_list"] = current_data["grocery_list"]

        self.save_data(data)

        self.item_feedback.configure(text="Item updated!", text_color="cyan")
        self.display_items()
        self.qty_entry_items.delete(0, END)
        
        self.filter_inventory(self.filter_dropdown.get())

    # delete specific item on button click from grocery list
    def delete_items(self, item_name):
        if item_name in current_data["grocery_list"]:
            del current_data["grocery_list"][item_name]
            self.item_feedback.configure(text="Successfully Deleted", text_color="orangered")
            
            # save to data.json file
            data = self.load_data()

            data[current_user]["grocery_list"] = current_data["grocery_list"]

            self.save_data(data)

        self.display_items()

        self.filter_inventory(self.filter_dropdown.get())

    # clear all items from grocery list
    def clear_all_items(self):
        current_data["grocery_list"].clear()

        data = self.load_data()

        data[current_user]["grocery_list"] = {}

        self.save_data(data)

        self.display_items()
        self.item_feedback.configure(text="All items cleared!", text_color="cyan")

    # the display widgets function
    def display_items(self):
        for widget in self.list_frame.winfo_children():
            if isinstance(widget, CTkLabel) or isinstance(widget, CTkButton):
                if widget.grid_info()['row'] != 0:  
                    widget.destroy()

        row = 1
        for item, details in current_data["grocery_list"].items():
            CTkLabel(self.list_frame, text=item).grid(row=row, column=0, padx=10, pady=5)
            CTkLabel(self.list_frame, text=details["category"]).grid(row=row, column=1, padx=10, pady=5)
            CTkLabel(self.list_frame, text=str(details["quantity"])).grid(row=row, column=2, padx=10, pady=5)

            delete_button = CTkButton(self.list_frame, text="Delete", width=60, command=lambda i=item: self.delete_items(i),fg_color="#B33939",hover_color="#E55039")
            delete_button.grid(row=row, column=3, padx=10, pady=5)

            row += 1
    
    def on_display(self):
        super().on_display()
        self.cat_dropdown_items.set("Select a Category")
        self.items_dropdown.set("Select Category First")
        self.filter_dropdown.set("All")
        self.display_items()
        self.filter_inventory("All")
        self.tkraise()

class BudgetMenu(ParentFrame):
    def __init__(self, master, controller):
        super().__init__(master, controller)

        # Main Widgets
        self.header = CTkLabel(self, text='Budget Tracker', font=controller.header_font)
        self.header.grid(row=0, column=0, pady=30, sticky='n')

        self.tabs = CTkTabview(self, corner_radius=30, )
        self.tabs.grid(row=0, column=0, rowspan=7, padx=15, pady=60, sticky='nsew')
        self.tabs.add('Income')
        self.income = self.tabs.tab('Income')
        self.income.grid_rowconfigure((0,1,2,3,4,5,6), weight=1, uniform='b')
        self.income.grid_columnconfigure(0, weight=1, uniform='b')
        self.tabs.add('Expenses')
        self.expenses = self.tabs.tab('Expenses')
        self.expenses.grid_rowconfigure((0,1,2,3,4,5,6), weight=1, uniform='a')
        self.expenses.grid_columnconfigure(0, weight=1, uniform='a')
        self.tabs.add('Overview')
        self.overview = self.tabs.tab('Overview')
        self.overview.grid_rowconfigure((0,1,2,3,4,5,6), weight=1, uniform='a')
        self.overview.grid_columnconfigure(0, weight=1, uniform='a')

        self.back = CTkButton(self, text='Back to Main Menu', width=100, height=50,
                               font=controller.subheader_font, command=lambda:controller.show_frame(MainMenu))
        self.back.grid(row=6, column=0)

        # Income Tab
        self.income_label = CTkLabel(self.income, text='Income Tracker', font=controller.header_font)
        self.income_label.grid(row=0, column=0, sticky='n')
        self.income_label2 = CTkFrame(self.income, width=190, height=2, fg_color=colors3)
        self.income_label2.grid(row=0, column=0, pady=(30, 0), sticky='n')
        self.source_label = CTkLabel(self.income, text='Source : ')
        self.source_label.grid(row=0, column=0, padx=(0, 160), pady=(30, 0), sticky='s')
        self.source_entry = CTkEntry(self.income, placeholder_text='Eg. Salary, Savings')
        self.source_entry.grid(row=0, column=0, padx=(50, 0), pady=(30, 0), sticky='s')
        self.amt_label = CTkLabel(self.income, text='Amount (RM) : ')
        self.amt_label.grid(row=1, column=0, padx=(0, 202.5), pady=(10, 0), sticky='n')
        self.amt_entry = CTkEntry(self.income, placeholder_text='Eg. 9999.99')
        self.amt_entry.grid(row=1, column=0, padx=(50, 0), pady=(10, 0), sticky='n')
        self.addincome_button = CTkButton(self.income, text='Add Income', command=self.add_income, font=controller.subheader_font)
        self.addincome_button.grid(row=1, column=0, pady=(60, 0), rowspan=2, sticky='n')
        self.income_feedback = CTkLabel(self.income, text='')
        self.income_feedback.grid(row=2, column=0)

        self.income_frame = CTkScrollableFrame(self.income, fg_color=colors2)
        self.income_frame.grid(row=3, column=0, rowspan=3, sticky='news')
        self.columns1 = ['Source', 'Amount', 'Date Added', 'Delete']
        for col, text in enumerate(self.columns1):
            self.label = CTkLabel(self.income_frame, text=text, fg_color=colors, corner_radius=5)
            self.label.grid(row=0, column=col, padx=10, pady=5, sticky='nsew')
            self.income_frame.grid_columnconfigure(col, weight=1)

        # Expenses Tab
        self.expense_label = CTkLabel(self.expenses, text='Expenses', font=controller.subheader_font)
        self.expense_label.grid(row=0, column=0, padx=(0, 150), sticky='ne')
        self.expense_label2 = CTkFrame(self.expenses, width=110, height=2, fg_color=colors3)
        self.expense_label2.grid(row=0, column=0, padx=(0, 135), pady=(27.5, 0), sticky='ne')
        self.item_label = CTkLabel(self.expenses, text='Item Name : ')
        self.item_label.grid(row=0, column=0, padx=(0, 230), sticky='se')
        self.item_entry = CTkEntry(self.expenses, placeholder_text='Eg. Milk')
        self.item_entry.grid(row=0, column=0, padx=(0, 80), sticky='se')
        self.category_label = CTkLabel(self.expenses, text='Category : ')
        self.category_label.grid(row=1, column=0, padx=(0, 230), sticky='ne')
        self.category_entry = CTkOptionMenu(self.expenses, values=['Food & Drinks', 'Entertainment', 'Shops', 'Rent', 'Utility', 'Others'])
        self.category_entry.grid(row=1, column=0, padx=(0, 80), sticky='ne')
        self.category_entry.set(value='')
        self.amount_label = CTkLabel(self.expenses, text='Amount (RM): ')
        self.amount_label.grid(row=1, column=0, padx=(0, 230), pady=(17.5, 0), sticky='e')
        self.amount_entry = CTkEntry(self.expenses, placeholder_text='Eg. 9999.99')
        self.amount_entry.grid(row=1, column=0, padx=(0, 80), pady=(17.5, 0), sticky='e')
        self.addexpense_button = CTkButton(self.expenses, text='Add Expenses', font=controller.subheader_font, command=self.add_expenses)
        self.addexpense_button.grid(row=2, column=0, padx=(0, 120), sticky='ne')
        self.expense_feedback = CTkLabel(self.expenses, text='', text_color='orangered')
        self.expense_feedback.grid(row=2, column=0, padx=(0, 105), pady=(20, 0), sticky='e')

        self.expense_frame = CTkScrollableFrame(self.expenses, fg_color=colors2)
        self.expense_frame.grid(row=3, column=0, rowspan=3, sticky='news')
        self.columns = ['Item Name', 'Category', 'Amount', 'Date Added', 'Delete']
        for col, text in enumerate(self.columns):
            self.label = CTkLabel(self.expense_frame, text=text, fg_color=colors, corner_radius=5)
            self.label.grid(row=0, column=col, padx=10, pady=5, sticky='nsew')
            self.expense_frame.grid_columnconfigure(col, weight=1)

        self.budget_label = CTkLabel(self.expenses, text='Budget Planner', font=controller.subheader_font)
        self.budget_label.grid(row=0, column=0, padx=(125, 0), sticky='nw')
        self.budget_label2 = CTkFrame(self.expenses, width=140, height=2, fg_color=colors3)
        self.budget_label2.grid(row=0, column=0, padx=(125, 0), pady=(27.5, 0), sticky='nw')
        self.category_label2 = CTkLabel(self.expenses, text='Category : ')
        self.category_label2.grid(row=0, column=0, padx=(75, 0), sticky='sw')
        self.category_entry2 = CTkOptionMenu(self.expenses, values=['Food & Drinks', 'Entertainment', 'Shops', 'Rent', 'Utility', 'Others'])
        self.category_entry2.grid(row=0, column=0, padx=(150, 0), sticky='sw')
        self.category_entry2.set(value='')
        self.budgetamt_label = CTkLabel(self.expenses, text='Amount (RM): ')
        self.budgetamt_label.grid(row=1, column=0, padx=(50, 0), pady=(20, 0), sticky='w')
        self.budgetamt_entry = CTkEntry(self.expenses, placeholder_text='Eg. 9999.99')
        self.budgetamt_entry.grid(row=1, column=0, padx=(150, 0), pady=(20, 0), sticky='w')
        self.budget_button = CTkButton(self.expenses, text='Set Budget', font=controller.subheader_font, command=self.set_budget)
        self.budget_button.grid(row=2, column=0, padx=(120, 0), sticky='nw')
        self.resetbudget_button = CTkButton(self.expenses, text='Reset', fg_color='transparent', width=50, hover=False, command=self.reset_budget)
        self.resetbudget_button.grid(row=2, column=0, padx=(0, 120), sticky='n')
        self.budget_feedback = CTkLabel(self.expenses, text='', text_color='orangered')

        # Overview Tab
        self.overview_label = CTkLabel(self.overview, text='Overview', font=controller.header_font)
        self.overview_label.grid(row=0, column=0, sticky='n')
        self.overview_label2 = CTkFrame(self.overview, width=150, height=2, fg_color=colors3)
        self.overview_label2.grid(row=0, column=0, sticky='n', pady=(30, 0))

        self.warning_category = ''
        self.warning_maxbudget = ''
        self.warning_msg = CTkLabel(self.overview, text='', text_color='orangered')
        self.warning_msg.grid(row=0, column=0, sticky='s')

        self.overview_frame = CTkScrollableFrame(self.overview)
        self.overview_frame.grid(row=1, column=0, rowspan=5, sticky='nsew')
        self.overview_frame.grid_rowconfigure((0,1,2,3,4,5,6,7,8,9,10), weight=1)
        self.overview_frame.grid_columnconfigure(0, weight=1)
        self.allbudget_label = CTkLabel(self.overview_frame, text='Allocated Budget: 0 / 0')
        self.allbudget_label.grid(row=0, column=0)
        self.allbudget_progbar = CTkProgressBar(self.overview_frame, width=400, height=20)
        self.allbudget_progbar.grid(row=1, column=0, pady=(0, 5))
        self.fd_label = CTkLabel(self.overview_frame, text='Food & Drinks: 0 / 0')
        self.fd_label.grid(row=2, column=0)
        self.fd_progbar = CTkProgressBar(self.overview_frame, width=400, height=20)
        self.fd_progbar.grid(row=3, column=0, pady=(0, 5))
        self.en_label = CTkLabel(self.overview_frame, text='Entertainment: 0 / 0')
        self.en_label.grid(row=4, column=0)
        self.en_progbar = CTkProgressBar(self.overview_frame, width=400, height=20)
        self.en_progbar.grid(row=5, column=0, pady=(0, 5))
        self.sh_label = CTkLabel(self.overview_frame, text='Shops: 0 / 0')
        self.sh_label.grid(row=6, column=0)
        self.sh_progbar = CTkProgressBar(self.overview_frame, width=400, height=20)
        self.sh_progbar.grid(row=7, column=0, pady=(0, 5))
        self.re_label = CTkLabel(self.overview_frame, text='Rent: 0 / 0')
        self.re_label.grid(row=8, column=0)
        self.re_progbar = CTkProgressBar(self.overview_frame, width=400, height=20)
        self.re_progbar.grid(row=9, column=0, pady=(0, 5))
        self.ut_label = CTkLabel(self.overview_frame, text='Utility: 0 / 0')
        self.ut_label.grid(row=10, column=0)
        self.ut_progbar = CTkProgressBar(self.overview_frame, width=400, height=20)
        self.ut_progbar.grid(row=11, column=0, pady=(0, 5))
        self.ot_label = CTkLabel(self.overview_frame, text='Others: 0 / 0')
        self.ot_label.grid(row=12, column=0)
        self.ot_progbar = CTkProgressBar(self.overview_frame, width=400, height=20)
        self.ot_progbar.grid(row=13, column=0, pady=(0, 5))
        self.spending_label = CTkLabel(self.overview_frame, text='Total Spending / Income: 0 / 0')
        self.spending_label.grid(row=14, column=0)
        self.spending_progbar = CTkProgressBar(self.overview_frame, width=400, height=20)
        self.spending_progbar.grid(row=15, column=0, pady=(0, 5))

        self.update_button = CTkButton(self.overview, text='Update', command=self.update_overview, font=controller.subheader_font)
        self.update_button.grid(row=6, column=0, sticky='e')

        self.append_widgets([self.source_entry, self.amt_entry, self.income_frame,
                                 self.item_entry, self.category_entry, self.amount_entry,
                                 self.expense_frame, self.category_entry2, self.budget_feedback,
                                 self.income_feedback, self.expense_feedback, self.budgetamt_entry,
                                 self.overview_frame])

    def add_income(self):
         # get value from input fields
        source = self.source_entry.get().strip()
        amount = self.amt_entry.get().strip()
        date = datetime.now().strftime('%d-%m-%Y')
        # check for empty input fields
        if source == '' or amount == '':
            self.income_feedback.configure(text='Please enter source and amount!', text_color='orangered')
            return
        # check if amount is valid integer
        try:
            float(amount)
        except ValueError:
            self.income_feedback.configure(text='Please enter a valid amount!', text_color='orangered')
            return
        # create data if empty
        if 'income' not in current_data:
            current_data['income'] = []
        # save data
        current_data['income'].append({
            'Source': source,
            'Amount': float(amount),
            'Date Added': date
        })
        rdata = self.load_data()
        rdata[current_user] = current_data
        self.save_data(rdata)

        # show feedback
        self.source_entry.delete(0, END)
        self.amt_entry.delete(0, END)
        self.focus()
        self.income_feedback.configure(text='Successfully added income!', text_color="#46BA46")
        self.reload_income()

    def reload_income(self):
        # clear the frame
        for v in self.income_frame.winfo_children():
            if isinstance(v, CTkFrame):
                v.destroy()
        # recreate the frame
        for v in current_data['income']:
            source = v['Source']
            amount = v['Amount']
            date = v['Date Added']
            self.new_income = CTkFrame(self.income_frame, fg_color=colors, corner_radius=5)
            row_index = len(self.income_frame.winfo_children()) - 4
            for c, value in enumerate((source, amount, date)):
                cell = CTkLabel(self.new_income, text=value if c != 1 else f'{value:.2f}')
                cell.grid(row=0,column=c, sticky='nsew')
                self.new_income.grid_columnconfigure(c, weight=1)
            self.delete_button = CTkButton(self.new_income, text='X', command=lambda i=self.new_income, s=source, a=amount, d=date: self.del_income(i, s, a, d)).grid(row=0, column=4, padx=10, pady=6, sticky='nsew')
            self.new_income.grid(row=row_index, column=0, columnspan=5, sticky='nsew')
        # set the overall budget (total income)
        current_data['overall_budget'] = 0
        for items in current_data['income']:
            current_data['overall_budget'] += items.get('Amount', 0)
        rdata = self.load_data()
        rdata[current_user] = current_data
        self.save_data(rdata)
        self.update_overview()

    def del_income(self, income_frame, source, amount, date):
        # delete frame
        income_frame.destroy()
        # remove data
        for i, v in enumerate(current_data['income']):
            if v['Source'] == source and v['Amount'] == amount and v['Date Added'] == date:
                del current_data['income'][i]
                break
        rdata = self.load_data()
        rdata[current_user] = current_data
        self.save_data(rdata)
        self.reload_income()

    def set_budget(self):
        # get values from input fields
        category = self.category_entry2.get().strip()
        amount = self.budgetamt_entry.get().strip()
        # check for empty entry fields
        if category == '' and amount == '':
            self.budget_feedback.grid(row=2, column=0, padx=(75, 0), pady=(20, 0), sticky='w')
            self.budget_feedback.configure(text='Please select a category and amount!', text_color='orangered')
            return
        elif category == '' and amount != '':
            self.budget_feedback.grid(row=2, column=0, padx=(110, 0), pady=(20, 0), sticky='w')
            self.budget_feedback.configure(text='Please select a category!', text_color='orangered')
            return
        elif category != '' and amount == '':
            self.budget_feedback.grid(row=2, column=0, padx=(110, 0), pady=(20, 0), sticky='w')
            self.budget_feedback.configure(text='Please enter an amount!', text_color='orangered')
            return
        # check if amount is valid integer
        try:
            float(amount)
        except ValueError:
            self.budget_feedback.grid(row=2, column=0, padx=(100, 0), pady=(20, 0), sticky='w')
            self.budget_feedback.configure(text='Amount must be a number!', text_color='orangered')
            return
        # check if exceed budget
        total = 0
        for amt in current_data['budgets'].values():
            total += amt
        total -= current_data['budgets'].get(category, 0)
        if (float(amount) + total) > current_data['overall_budget']:
            self.budget_feedback.grid(row=2, column=0, padx=(50, 0), pady=(20, 0), sticky='w')
            self.budget_feedback.configure(text=f"Desired budget exceed maximum budget of {current_data['overall_budget']}", text_color='orangered')
            return
        # write back into json file
        current_data['budgets'][category] = float(amount)
        rdata = self.load_data()
        rdata[current_user] = current_data
        self.save_data(rdata)
        # show feedback
        self.category_entry2.set('')
        self.budgetamt_entry.delete(0, END)
        self.focus()
        self.budget_feedback.grid(row=2, column=0, padx=(100, 0), pady=(20, 0), sticky='w')
        self.budget_feedback.configure(text='Budget successfully updated!', text_color="#46BA46")
        self.update_overview()

    def reset_budget(self):
        # Ask for confirmation
        answer = messagebox.askyesno('Confirm', 'Are you sure you want to reset all budget set?')
        if answer:
            for v in current_data['budgets']:
                current_data['budgets'][v] = 0
            self.budget_feedback.grid(row=2, column=0, padx=(100, 0), pady=(20, 0), sticky='w')
            self.budget_feedback.configure(text='Budget successfully resetted!', text_color="#46BA46")

            rdata = self.load_data()
            rdata[current_user] = current_data
            self.save_data(rdata)
        self.update_overview()

    def add_expenses(self):
        # get values from input fields
        item = self.item_entry.get().strip()
        category = self.category_entry.get().strip()
        amount = self.amount_entry.get().strip()
        date = datetime.now().strftime('%d-%m-%Y')
        # check for empty entry fields
        if item == '' or category == '' or amount == '':
            self.expense_feedback.configure(text='Please enter all input fields!', text_color='orangered')
            return
        # check if amount is valid integer
        try:
            float(amount)
        except ValueError:
            self.expense_feedback.configure(text='Please enter a valid amount!', text_color='orangered')
            return
        # check if exceeds budget
        total = 0
        for amt in current_data['expenses']:
            if amt.get('Category') == category:
                total = amt.get('Amount', 0)
        if (float(amount) + total) > current_data['budgets'].get(category, 0):
            self.expense_feedback.configure(text=f'Item exceeds {category} budget!', text_color='orangered')
            return
        # create data if empty
        if 'expenses' not in current_data:
            current_data['expenses'] = []
        # save data 
        current_data['expenses'].append({
            'Item Name': item,
            'Category': category,
            'Amount': float(amount),
            'Date Added': date
        })
        rdata = self.load_data()
        rdata[current_user] = current_data
        self.save_data(rdata)
        # show feedback
        self.item_entry.delete(0, END)
        self.category_entry.set('')
        self.amount_entry.delete(0, END)
        self.focus()
        self.expense_feedback.configure(text='Successfully added expenses!', text_color="#46BA46")
        self.reload_expense()

    def reload_expense(self):
        # clear the frame
        for v in self.expense_frame.winfo_children():
            if isinstance(v, CTkFrame):
                v.destroy()
        # recreate frames
        for v in current_data['expenses']:
            item = v['Item Name']
            category = v['Category']
            amount = v['Amount']
            date = v['Date Added']
            self.new_expense = CTkFrame(self.expense_frame, fg_color=colors, corner_radius=5)
            self.new_expense.grid_columnconfigure((0,1,2,3,4), weight=1)
            widths = (100, 90, 80, 100)
            row_index = len(self.expense_frame.winfo_children()) - 5
            for c, value in enumerate((item, category, amount, date)):
                cell = CTkLabel(self.new_expense, width=widths[c], text=value if c != 2 else f'{value:.2f}')
                cell.grid(row=0,column=c, padx=10, sticky='nsew')
            self.delete_button = CTkButton(self.new_expense, width=60, text='X', command=lambda f=self.new_expense, i=item, cat=category, amt=amount, d=date: self.del_expense(f, i, cat, amt, d))
            self.delete_button.grid(row=0, column=4, padx=(20, 15), sticky='nsew')
            self.new_expense.grid(row=row_index, column=0, columnspan=5, sticky='nsew')
        self.update_overview()

    def del_expense(self, expense_frame, item, category, amount, date):
        # delete frame
        expense_frame.destroy()
        # remove data
        for i, v in enumerate(current_data['expenses']):
            if v['Item Name'] == item and v['Category'] == category and v['Amount'] == amount and v['Date Added'] == date:
                del current_data['expenses'][i]
                break
        rdata = self.load_data()
        rdata[current_user] = current_data
        self.save_data(rdata)

        self.reload_expense()

    def update_overview(self):
        # Clear message warning string
        self.warning_maxbudget = ''
        self.warning_category = ''
        # Update progress bar and warning message
        self.update_progbar(self.allbudget_progbar, self.allbudget_label, 'Allocated Budget', mode = 'budget')
        self.update_progbar(self.fd_progbar, self.fd_label, 'Food & Drinks')
        self.update_progbar(self.en_progbar, self.en_label, 'Entertainment')
        self.update_progbar(self.sh_progbar, self.sh_label, 'Shops')
        self.update_progbar(self.re_progbar, self.re_label, 'Rent')
        self.update_progbar(self.ut_progbar, self.ut_label, 'Utility')
        self.update_progbar(self.ot_progbar, self.ot_label, 'Others')
        self.update_progbar(self.spending_progbar, self.spending_label, 'Total Spending over Income', mode = 'expenses')
        self.warning_categories = f'Expenses in {self.warning_category}exceed their respective budget!' if self.warning_category else ''
        self.warning_msg.configure(text=f'Warning: {self.warning_maxbudget} {self.warning_categories}' if self.warning_maxbudget or self.warning_category else f'')

    def update_progbar(self, progress_bar, label, category, mode = 'category'):
        # get value based on mode (budget, category, expenses)
        value = 0
        if mode == 'budget':
            value = sum(current_data['budgets'].values())
        else:
            expenses = current_data['expenses']
            if mode == 'category':
                value = sum(v.get('Amount', 0) for v in expenses if v.get('Category') == category)
            elif mode == 'expenses':
                value = sum(v.get('Amount', 0) for v in expenses)
            
        # append the words to be displayed as warning message (default: '')
        if mode == 'category':
            if value > current_data['budgets'].get(category): self.warning_category += ', ' + category + ' 'if self.warning_category else category + ' '
        if mode == 'budget':
            if value > current_data['overall_budget']: self.warning_maxbudget = 'Budgets Set exceed Maximum Budget!'

        # get percentage / ratio for progress bar
        if mode == 'budget' or mode == 'expenses':
            if current_data.get('overall_budget', 0) == 0: #avoid zero division
                ratio = 0 if value == 0 else 1
            else:
                ratio = value / current_data['overall_budget']
        else:
            if current_data['budgets'].get(category, 0) == 0:
                ratio = 0 if value == 0 else 1
            else:
                ratio = value / current_data['budgets'].get(category)
        # get color for progress bar
        if ratio > 1: ratio = 1 # max ratio = 1
        if ratio < 0.5:
            r = int(255 * (ratio/0.5))
            g = 255
        else:
            r = 255
            g = int(255 * (1 - (ratio - 0.5) / 0.5))
        color = f'#{r:02x}{g:02x}00'
        # set values
        progress_bar.set(ratio)
        progress_bar.configure(progress_color=color)
        if mode == 'budget' or mode == 'expenses':
            label.configure(text=f"{category} : {value:.2f} / {current_data['overall_budget']:.2f}")
        elif mode == 'category':
            label.configure(text=f"{category} : {value:.2f} / {current_data['budgets'][category]:.2f}")

    def on_display(self):
        super().on_display()
        self.tabs.set('Income')
        self.reload_income()
        self.reload_expense()
        self.update_overview()

class MealMenu(ParentFrame):
    def __init__(self, master, controller):
        super().__init__(master, controller)

        self.label = CTkLabel(self, text="Meal Planner System", font=controller.header_font)
        self.label.grid(row=0, column=0)
        self.clear_plan_button = CTkButton(self, text='Clear Plan', command=self.clear_plan)
        self.clear_plan_button.grid(row=1, column=0, padx=(0, 15), pady=(5,0), sticky='ne')

        self.frame = CTkFrame(self, width=100, height=500,corner_radius=20)
        self.frame.grid(row=1,column=0, padx=(20, 0), rowspan=7,sticky='w')

        self.result_frame = CTkScrollableFrame(self, width=500, height=500,corner_radius=20)
        self.result_frame.grid(row=1,column=0,padx=(0, 20), rowspan=7,sticky='e')
        self.result_frame.grid_rowconfigure(0, weight=1)
        self.result_frame.grid_columnconfigure(0, weight=1)
        self.result_label_created = False
        
        self.result_label = CTkLabel(self.result_frame, text='', justify='center')
        self.result_label.grid(row=0, column=0)
        
        #Choose Gender
        GenderLabel = CTkLabel(self.frame, text="Gender")
        GenderLabel.grid(row=1, column=0)
        Gender = ["Male","Female"]
        self.Gender_Var = StringVar(value="Male")
        GenderChoose = CTkComboBox(self.frame, values=Gender, variable=self.Gender_Var, state="readonly")
        GenderChoose.grid(row=2, column=0)
        # Input Age
        AgeLabel = CTkLabel(self.frame, text="Age")
        AgeLabel.grid(row=3, column=0,pady=(10,0))
        self.Age = CTkEntry(self.frame)
        self.Age.grid(row=4, column=0)
        # Input Height
        HeightLabel = CTkLabel(self.frame, text="Height(cm)")
        HeightLabel.grid(row=5, column=0,pady=(10,0))
        self.Height = CTkEntry(self.frame)
        self.Height.grid(row=6, column=0)
        # Input Weight
        WeightLabel = CTkLabel(self.frame, text="Weight(Kg)")
        WeightLabel.grid(row=7, column=0,pady=(10,0))
        self.Weight = CTkEntry(self.frame)
        self.Weight.grid(row=8, column=0)
        # Choose Daily Activity
        DailyLabel = CTkLabel(self.frame, text="Daily activity")
        DailyLabel.grid(row=9, column=0,pady=(10,0))
        Activity = ["Long Time Sit","Low active","Mid Active","High Active","Athelete Level"]
        self.Activity_Var = StringVar(value="Long Time Sit")
        DailyChoose = CTkComboBox(self.frame, values=Activity, variable=self.Activity_Var, state="readonly")
        DailyChoose.grid(row=10, column=0)
        # Choose Illness if user have
        IllLabel = CTkLabel(self.frame, text="Illness(if have)")
        IllLabel.grid(row=11, column=0,pady=(10,0))
        Illness = ["None","Diabetes","High Blood Pressure","High Cholesterol"]
        self.Illness_Var = StringVar(value="None")
        IllChoose = CTkComboBox(self.frame, values=Illness, variable=self.Illness_Var, state="readonly")
        IllChoose.grid(row=12, column=0)
        # Choose Target
        TargetLabel = CTkLabel(self.frame,text="Target")
        TargetLabel.grid(row=13, column=0,pady=(10,0))
        Target = ["Lose Weight","Gain Weight","Maintain"]
        self.Target_Var = StringVar(value="Lose Weight")
        TargetChoose = CTkComboBox(self.frame, values=Target, variable=self.Target_Var, state="readonly")
        TargetChoose.grid(row=14, column=0)

        # Specific Requirements
        SRLabel = CTkLabel(self.frame,text="Specific Requirements")
        SRLabel.grid(row=15, column=0,pady=(10,0))
        Special = ["None","Vegetarian Diet","Halal"]
        self.Special_Var = StringVar(value="None")
        SRChoose = CTkComboBox(self.frame, values=Special, variable=self.Special_Var, state="readonly")
        SRChoose.grid(row=16, column=0)

        self.submitButton = CTkButton(self.frame,text="Submit",command = self.submit)
        self.submitButton.grid(row=17, column=0, padx=20, pady=20)

        self.decide = CTkButton(self, text="Back to Main Menu", command=lambda:controller.show_frame(MainMenu), font=controller.subheader_font,width=100,height=50)
        self.decide.grid(row=6, column=0, pady=(50, 0))

        self.breakfast_fruits = ["Apple","Orange","Banana","Blueberry","Kiwi","Avocado","Grapes","Papaya","Mango","Strawberry"]
        self.breakfast_oats = ["Whole wheat bread","Oats","Corn","Pumpkin","Sweet Potato"]
        self.breakfast_meat = ["Bacon","Steak","Sausage","Chicken Breast","Ham","Salmon"]
        self.breakfast_protein = ["Egg(scrambled/boiled)","Greek yogurt"]
        self.meat = ["Bacon","Steak","Sausage","Chicken Breast","Ham","Salmon"]
        self.qualified_meat = [x for x in self.meat if x not in ["Bacon","Sausage","Ham"]]
        self.vegetable = ["Broccoli","Salad","Cucumber","Eggplant","Potatoes","Pumpkin","Corn"]
        self.protein = ["Egg","Tofu","Black Bean","Walnut","Almond","Pine Nut","Hazelnut"]


    def calculate_BMR(self,gender,age,height,weight):
        if gender == "Male":
            return 10 * weight + 6.25 * height - 5 * age +5
        else:
            return 10 * weight + 6.25 * height - 5 * age - 161

    def activity_factor(self,Level):
        factors = {
                "Long Time Sit": 1.2,
                "Low active": 1.375,
                "Mid Active": 1.55,
                "High Active": 1.725,
                "Athelete Level": 1.9,
            }
        return factors.get(Level, 1.2)

    def submit(self):
        try:
            gender = self.Gender_Var.get()
            age = int(self.Age.get())
            if age == 0:
                messagebox.showerror(title="Wrong Value",message="Age cannot be 0, please enter again!")
                return
            if age < 0:
                messagebox.showerror(title="Wrong Value",message="Age cannot be less than 0, please enter again!")
                return
        except ValueError:
            messagebox.showerror(title="Wrong Value",message="Wrong value for Age, please enter again!")
            return
        try:
            height = float(self.Height.get())
            if height == 0:
                messagebox.showerror(title="Wrong Value",message="Height cannot be 0, please enter again")
                return
            if height < 0:
                messagebox.showerror(title="Wrong Value",message="Height cannot be less than 0, please enter again!")
                return
        except ValueError:
            messagebox.showerror(title="Wrong Value",message="Wrong value for Height, please enter again!")
            return
        try:
            weight = float(self.Weight.get())
            if weight == 0:
                messagebox.showerror(title="Wrong Value",message="Weight cannot be 0, please enter again!")
                return
            if weight < 0:
                messagebox.showerror(title="Wrong Value",message="Weight cannot be less than 0, please enter again!")
                return
        except ValueError:
            messagebox.showerror(title="Wrong Value",message="Wrong value for Weight, please enter again!")
            return
        else:
            activity = self.Activity_Var.get()
            target = self.Target_Var.get()
            
        BMR = self.calculate_BMR(gender,age,height,weight)
        TDEE = BMR * self.activity_factor(activity)

        if target == "Lose Weight":
            calories_need = TDEE - 300
        elif target == "Gain Weight":
            calories_need = TDEE + 300
        else:
            calories_need = TDEE

        if activity == "Long Time Sit" or activity == "Low active":
            protein = weight * 0.8
        else:
            protein = weight * 1.5
            
        fat = calories_need * 0.20 / 9
        carbs = calories_need / 2 / 4

        result_text = (
                    f"— Result —\n"
                    f"BMR(basal metabolic rate): {BMR:.2f} kcal\n"
                    f"TDEE(Total Daily Energy Expenditure): {TDEE:.2f} kcal\n"
                    f"Calories intake: {calories_need:.2f} kcal\n\n"
                    f"— Nutrition intake —\n"
                    f"Protein: {protein:.1f} g\n"
                    f"Fat: {fat:.1f} g\n"
                    f"Carbohydrates: {carbs:.1f} g"
                    + self.weekly_meal_plan()
                )
        if self.result_label_created == False:
            self.display_plan(result_text)
            self.result_label_created = True
            # save data into file
            rdata = self.load_data()
            rdata[current_user]['meal_plan'] = result_text
            self.save_data(rdata)
        else:
            self.display_plan(result_text)

    def clear_plan(self):
        rdata = self.load_data()
        if rdata[current_user].get('meal_plan', '') == '':
            messagebox.showerror(title='Data not Found', message='You currently don\'t have an existing meal plan!')
            return

        confirm = messagebox.askyesno(title='Confirmation', message='Are you sure you want to clear the current plan?')
        if confirm:  
            self.result_label_created = False
            self.result_label.configure(text='')
            rdata[current_user]['meal_plan'] = ''
            self.save_data(rdata)

    def display_plan(self, result):
        if result:
            self.result_label.configure(text=result)
        else:
            rdata = self.load_data()
            plan = rdata[current_user].get('meal_plan', {})
            self.result_label.configure(text=plan)

    def weekly_meal_plan(self):
        week_text = "\n— 7 Days Meal Plan —\n"

        for day in range(1, 8):
            day_plan = self.meal_plan()
            week_text += f"\nDay {day}\n{day_plan}\n"

        return week_text

    def meal_plan(self):
        illness = self.Illness_Var.get()
        special = self.Special_Var.get()
            
        if illness == "Diabetes":
                
            if special == "Vegetarian Diet":
                breakfast = [random.choice(self.breakfast_fruits)]
                breakfast.extend(random.sample(self.breakfast_oats,2))
                lunch = [random.choice(self.protein)]
                lunch.extend(random.sample(self.vegetable,2))
                dinner = [random.choice(self.protein)]
                dinner.extend(random.sample(self.vegetable,2))

            elif special == "Halal":
                breakfast = [random.choice(self.breakfast_fruits),random.choice(self.breakfast_oats),random.choice(self.qualified_meat)+"(steamed,poached)"]
                lunch = [random.choice(self.vegetable),random.choice(self.qualified_meat)+"(steamed,poached)",random.choice(self.protein)]
                dinner = [random.choice(self.vegetable),random.choice(self.qualified_meat)+"(steamed,poached)",random.choice(self.protein)]
                
            else :
                breakfast = [random.choice(self.breakfast_fruits),random.choice(self.breakfast_oats),random.choice(self.meat)+"(steamed,poached)"]
                lunch = [random.choice(self.vegetable),random.choice(self.meat)+"(steamed,poached)",random.choice(self.protein)]
                dinner = [random.choice(self.vegetable),random.choice(self.meat)+"(steamed,poached)",random.choice(self.protein)]

        elif illness == "High Blood Pressure":

            if special == "Vegetarian Diet":
                breakfast = [random.choice(self.breakfast_fruits)]
                breakfast.extend(random.sample(self.breakfast_oats,2))
                lunch = [random.choice(self.protein)]
                lunch.extend(random.sample(self.vegetable,2))
                dinner = [random.choice(self.protein)]
                dinner.extend(random.sample(self.vegetable,2))

            elif special == "Halal":
                breakfast = [random.choice(self.breakfast_fruits),random.choice(self.breakfast_oats),random.choice(self.qualified_meat)+"(steamed,poached)"]
                lunch = [random.choice(self.vegetable),random.choice(self.qualified_meat)+"(steamed,poached)",random.choice(self.protein)]
                dinner = [random.choice(self.vegetable),random.choice(self.qualified_meat)+"(steamed,poached)",random.choice(self.protein)]
                
            else :
                breakfast = [random.choice(self.breakfast_fruits),random.choice(self.breakfast_oats),random.choice(self.meat)+"(steamed,poached)"]
                lunch = [random.choice(self.vegetable),random.choice(self.meat)+"(steamed,poached)",random.choice(self.protein)]
                dinner = [random.choice(self.vegetable),random.choice(self.meat)+"(steamed,poached)",random.choice(self.protein)]

        elif illness == "High Cholesterol":

            if special == "Vegetarian Diet":
                breakfast = [random.choice(self.breakfast_fruits)]
                breakfast.extend(random.sample(self.breakfast_oats,2))
                lunch = [random.choice(self.protein)]
                lunch.extend(random.sample(self.vegetable,2))
                dinner = [random.choice(self.protein)]
                dinner.extend(random.sample(self.vegetable,2))

            elif special == "Halal":
                    breakfast = [random.choice(self.breakfast_fruits),random.choice(self.breakfast_oats),random.choice(self.qualified_meat)+"(steamed,poached)"]
                    lunch = [random.choice(self.vegetable),random.choice(self.qualified_meat)+"(steamed/poached)",random.choice(self.protein)]
                    dinner = [random.choice(self.vegetable),random.choice(self.qualified_meat)+"(steamed,poached)",random.choice(self.protein)]
                
            else :
                    breakfast = [random.choice(self.breakfast_fruits),random.choice(self.breakfast_oats),random.choice(self.meat)+"(steamed,poached)"]
                    lunch = [random.choice(self.vegetable),random.choice(self.meat)+"(steamed,poached)",random.choice(self.protein)]
                    dinner = [random.choice(self.vegetable),random.choice(self.meat)+"(steamed,poached)",random.choice(self.protein)]
                
        else:
            if special == "Vegetarian Diet":
                    breakfast = [random.choice(self.breakfast_fruits)]
                    breakfast.extend(random.sample(self.breakfast_oats,2))
                    lunch = [random.choice(self.protein)]
                    lunch.extend(random.sample(self.vegetable,2))
                    dinner = [random.choice(self.protein)]
                    dinner.extend(random.sample(self.vegetable,2))

            elif special == "Halal":
                    breakfast = [random.choice(self.breakfast_fruits),random.choice(self.breakfast_oats),random.choice(self.qualified_meat),]
                    lunch = [random.choice(self.vegetable),random.choice(self.qualified_meat),random.choice(self.protein)]
                    dinner = [random.choice(self.vegetable),random.choice(self.qualified_meat),random.choice(self.protein)]
                
            else :
                    breakfast = [random.choice(self.breakfast_fruits),random.choice(self.breakfast_oats),random.choice(self.meat)]
                    lunch = [random.choice(self.vegetable),random.choice(self.meat),random.choice(self.protein)]
                    dinner = [random.choice(self.vegetable),random.choice(self.meat),random.choice(self.protein)]

        return (
            f"\n— Recommended Meal —\n"
            f"Breakfast: {', '.join(map(str, breakfast))}\n"
            f"Lunch: {', '.join(map(str, lunch))}\n"
            f"Dinner: {', '.join(map(str, dinner))}"
        )

    def on_display(self):
        super().on_display()
        self.display_plan(None)

# Main Application (Handles all frames)
class App(CTk):
    def __init__(self):
        super().__init__()

        # Setup
        self.geometry('800x750')
        self.title('Neatly - Household Management App')
        self.resizable(False, False)
        self.grid_rowconfigure(0, weight = 1)
        self.grid_columnconfigure(0, weight = 1)

        # Fonts
        self.underlined = CTkFont(family='Tahoma', size=14, underline = True)
        self.bold = CTkFont(family='Tahoma', size=14, weight='bold')
        self.header_font = CTkFont(family='Tahoma', size=24, weight='bold')
        self.subheader_font = CTkFont(family='Tahoma', size=18, weight='bold')

        self.button = CTkButton(self, text='Dark Mode', width=80, height=20, bg_color=colors2, command=self.change_appearance_mode)
        self.button.grid(row=0, column=0, sticky='ne', padx=20, pady=20)

        self.frames = {} # dictionary to store frame classes

        for f in (LoginMenu, SignupMenu, MainMenu, GroceryMenu, BudgetMenu, MealMenu):
            frame = f(self, self)  # f(master, controller)
            self.frames[f] = frame # add to dictionary
            frame.grid(row=0, column=0, sticky='nsew')

        self.show_frame(LoginMenu)
        
        # Run (Main Loop)
        self.mainloop()

    # Methods (Menu Control)
    def show_frame(self, frame_class):
        frame = self.frames[frame_class]
        frame.on_display()
        self.button.tkraise()
        self.focus()
        
    def change_appearance_mode(self):
        app_mode = get_appearance_mode()
        if app_mode == 'Dark':
            self.button.configure(text = 'Light Mode')
            set_appearance_mode('light')

        elif app_mode == 'Light':
            self.button.configure(text = 'Dark Mode')
            set_appearance_mode('dark')

if __name__ == '__main__':
    app = App()
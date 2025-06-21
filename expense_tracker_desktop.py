import tkinter as tk
from tkinter import ttk
import os
from db_config import DB_PATH
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from PIL import Image
import io
import pandas as pd
import ttkbootstrap as ttk  # Replace tkinter.ttk with ttkbootstrap
from ttkbootstrap.constants import *  # Import ttkbootstrap constants
from ttkbootstrap.style import Style

METALLIC_GREY = "#71797E"  # For text and borders
OCEAN_BLUE = "#0077BE"     # For buttons and accents
LIGHT_GREY = "#F5F5F5"     # For hover effects
WHITE = "#FFFFFF"          # For background

class ExpenseTrackerApp:
    def __init__(self, root):
        # Create custom theme
        self.style = Style()
        
        # Configure base button style
        self.style.configure(
            "Custom.TButton",
            background=OCEAN_BLUE,
            foreground=WHITE,
            bordercolor=OCEAN_BLUE,
            focuscolor=OCEAN_BLUE,
            font=('Helvetica', 10)
        )
        
        # Use style map for button hover
        self.style.map("Custom.TButton",
            background=[("active", LIGHT_GREY)],
            foreground=[("active", OCEAN_BLUE)],
            bordercolor=[("active", OCEAN_BLUE)]
        )
        
        # Update frame style to white background
        self.style.configure(
            "Custom.TFrame",
            background=WHITE
        )
        
        # Update label style
        self.style.configure(
            "Custom.TLabel",
            background=WHITE,
            foreground=METALLIC_GREY
        )
        
        # Update entry style
        self.style.configure(
            "Custom.TEntry",
            fieldbackground=WHITE,
            foreground=METALLIC_GREY
        )
        
        # Update treeview style
        self.style.configure(
            "Custom.Treeview",
            background=WHITE,
            fieldbackground=WHITE,
            foreground=METALLIC_GREY,
            selectbackground=OCEAN_BLUE,
            selectforeground=WHITE
        )
        
        # Update labelframe style
        self.style.configure(
            "Custom.TLabelframe",
            background=WHITE,
            foreground=METALLIC_GREY
        )
        
        # Update labelframe label style
        self.style.configure(
            "Custom.TLabelframe.Label",
            background=WHITE,
            foreground=METALLIC_GREY,
            font=('Helvetica', 10, 'bold')
        )
        
        # Update treeview heading style
        self.style.configure(
            "Custom.Treeview.Heading",
            background=OCEAN_BLUE,
            foreground=WHITE,
            relief="flat"
        )
        
        # Apply theme to root window
        self.root = root
        self.root.title("💰 Expense Tracker")
        self.root.geometry("800x600")
        self.root.configure(bg=WHITE)  # Set root background to white
        
        # Main container with white background
        self.main_container = ttk.Frame(
            self.root,
            padding="20",
            style="Custom.TFrame"
        )
        self.main_container.grid(
            row=0,
            column=0,
            sticky=(tk.W, tk.E, tk.N, tk.S),
            padx=20,
            pady=20
        )
        
        # Configure grid weights for responsive design
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        # Create data directory if it doesn't exist
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        
        # Initialize database if it doesn't exist
        self.initialize_database()
        
        self.current_user = None
        
        # Initially show login frame
        self.show_login_frame()

    def show_login_frame(self):
        """Show the login frame with custom styling"""
        self.fade_out_widgets()
        
        # Login frame with custom styling
        login_frame = ttk.Frame(self.main_container, padding="20", style="Custom.TFrame")
        login_frame.grid(row=0, column=0, padx=20, pady=20)
        
        # Welcome header
        ttk.Label(
            login_frame,
            text="Welcome Back!",
            font=('Helvetica', 24, 'bold'),
            style="Custom.TLabel"
        ).grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Username
        ttk.Label(login_frame, text="👤 Username:", style="Custom.TLabel").grid(row=1, column=0, pady=5)
        self.username_var = tk.StringVar()
        username_entry = ttk.Entry(
            login_frame,
            width=30,
            style="Custom.TEntry",
            textvariable=self.username_var
        )
        username_entry.grid(row=1, column=1, pady=5)
        
        # Password
        ttk.Label(login_frame, text="🔒 Password:", style="Custom.TLabel").grid(row=2, column=0, pady=5)
        self.password_var = tk.StringVar()
        password_entry = ttk.Entry(
            login_frame,
            show="•",
            width=30,
            style="Custom.TEntry",
            textvariable=self.password_var
        )
        password_entry.grid(row=2, column=1, pady=5)
        
        # Button frame
        button_frame = ttk.Frame(login_frame, style="Custom.TFrame")
        button_frame.grid(row=3, column=0, columnspan=2, pady=20)
        
        # Login button
        login_btn = ttk.Button(
            button_frame,
            text="Login",
            command=self.login,
            style="Custom.TButton",
            width=15
        )
        login_btn.pack(side='left', padx=5)
        
        # Register button
        register_btn = ttk.Button(
            button_frame,
            text="Register",
            command=self.show_register_frame,
            style="Custom.TButton",
            width=15
        )
        register_btn.pack(side='left', padx=5)
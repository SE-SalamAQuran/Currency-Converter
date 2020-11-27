# # Python Project on Currency Converter
# # SALAM A QURAN
# # Made using tkinter and requests packages to access fixer api to get currencies live rates

from logging import raiseExceptions
import IPython as ip
import os
from os import access
from dotenv import load_dotenv
from easy_exceptions import EasyException

load_dotenv()
import matplotlib as mpl

mpl.use("TKAGG")
print(mpl.get_backend())

import requests
import tkinter as tk
from tkinter import ttk
from tkinter import StringVar, mainloop
import regex as re


class RealTimeCurrencyConverter:
    rates = {}

    def __init__(self, url):
        data = requests.get(url).json()
        self.rates = data["rates"]

    def convert(self, from_currency, to_currency, amount):
        initial_amount = amount
        if from_currency != "USD":  # USD is the default currency
            amount = amount / self.currencies[from_currency]

        # limiting the precision to 2 decimal places
        amount = round(amount * self.currencies[to_currency], 2)
        return amount


class App(tk.Tk):
    def __init__(self, converter):
        tk.Tk.__init__(self)
        self.title = "Currency Converter"
        self.currency_converter = converter
        s = ttk.Style()
        s.theme_use("equilux")

        self.geometry("500x200")

        # Label
        self.intro_label = tk.Label(
            self,
            text="Welcome to Real Time Currency Convertor",
            fg="blue",
            relief=tk.RAISED,
            borderwidth=3,
        )
        self.intro_label.config(font=("Courier", 15, "bold"))

        self.date_label = tk.Label(
            self,
            text=f"1 Indian Rupee equals = {self.currency_converter.convert('INR','USD',1)} USD \n Date : {self.currency_converter.data['date']}",
            relief=tk.GROOVE,
            borderwidth=5,
        )

        self.intro_label.place(x=10, y=5)
        self.date_label.place(x=160, y=50)

        # Entry box
        valid = (self.register(self.restrictNumberOnly), "%d", "%P")
        self.amount_field = tk.Entry(
            self,
            bd=3,
            relief=tk.RIDGE,
            justify=tk.CENTER,
            validate="key",
            validatecommand=valid,
        )
        self.converted_amount_field_label = tk.Label(
            self,
            text="",
            fg="black",
            bg="white",
            relief=tk.RIDGE,
            justify=tk.CENTER,
            width=17,
            borderwidth=3,
        )

        # dropdown
        self.from_currency_variable = StringVar(self)
        self.from_currency_variable.set("INR")  # default value
        self.to_currency_variable = StringVar(self)
        self.to_currency_variable.set("USD")  # default value

        font = ("Courier", 12, "bold")
        self.option_add("*TCombobox*Listbox.font", font)
        self.from_currency_dropdown = ttk.Combobox(
            self,
            textvariable=self.from_currency_variable,
            values=list(self.currency_converter.currencies.keys()),
            font=font,
            state="readonly",
            width=12,
            justify=tk.CENTER,
        )
        self.to_currency_dropdown = ttk.Combobox(
            self,
            textvariable=self.to_currency_variable,
            values=list(self.currency_converter.currencies.keys()),
            font=font,
            state="readonly",
            width=12,
            justify=tk.CENTER,
        )

        # placing
        self.from_currency_dropdown.place(x=30, y=120)
        self.amount_field.place(x=36, y=150)
        self.to_currency_dropdown.place(x=340, y=120)
        # self.converted_amount_field.place(x = 346, y = 150)
        self.converted_amount_field_label.place(x=346, y=150)

        # Convert button
        self.convert_button = tk.Button(
            self, text="Convert", fg="black", command=self.perform
        )
        self.convert_button.config(font=("Courier", 10, "bold"))
        self.convert_button.place(x=225, y=135)

    def perform(self):
        amount = float(self.amount_field.get())
        from_curr = self.from_currency_variable.get()
        to_curr = self.to_currency_variable.get()

        converted_amount = self.currency_converter.convert(from_curr, to_curr, amount)
        converted_amount = round(converted_amount, 2)

        self.converted_amount_field_label.config(text=str(converted_amount))

    def restrictNumberOnly(self, action, string):
        regex = re.compile(r"[0-9,]*?(\.)?[0-9,]*$")
        result = regex.match(string)
        return string == "" or (string.count(".") <= 1 and result is not None)


# Driver code
if __name__ == "__main__":

    ACCESS_KEY = os.getenv("MY_API_KEY")
    url = str.__add__("https://fixer.io/api/latest?access_key=", ACCESS_KEY)
    converter = RealTimeCurrencyConverter(url)

    App(converter)
    mainloop()

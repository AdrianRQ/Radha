import pandas as pd
import sqlite3
from pattern.en import number, pluralize
from num2words import num2words

input_str = input("Enter ingredient str:")

conn = sqlite3.connect('test_database')

def fetch_ingredients():
    ing_list = pd.read_sql_query("SELECT Ingredient FROM ingredients", conn)['Ingredient'].tolist()
    return ing_list

def fetch_units():
    unit_list = pd.read_sql_query("SELECT Symbol FROM units", conn)['Symbol'].tolist()
    return list(filter(None, [x for x in unit_list if (x != '')])) 

def match_ingredient(input_str, ing_list):
    matches = [ing.lower() for ing in ing_list if ing.lower() in input_str.lower()]
    return max(matches, key=len)

def check_plural(input_str, ing_matched):
    if pluralize('ing_matched') in input_str.lower():
        return(pluralize('ing_matched'))
    else:
        return ing_matched

def get_digits(input_str):
    digits_list = [s for s in input_str.split() if s.isdigit()]
    if len(digits_list)==1:
        return digits_list[0]
    elif len(digits_list)==0:
        return ''
    else:
        for i in range(0, len(digits_list)):
            new_dig = digits_list[0]
            if ' '.join(digits_list[:i]) in input_str:
                new_dig = ' '.join(digits_list[:i])
            else:
                break
        return new_dig

def get_number_words(input_str):
    num = number(input_str)
    numword = num2words(num)
    if numword in input_str:
        return numword
    else:
        return ''

def match_units(input_str, units_list):
    input_list = input_str.lower().split()
    for word in input_list:
        if word in units_list:
            return word
    return ''  
   

ing_list = fetch_ingredients()
units_list = fetch_units()

input_str = input_str.lower()

ingredient = match_ingredient(input_str, ing_list)
product = check_plural(input_str, ingredient)

input_str = input_str.replace(product, '').replace('  ', ' ')

quantity = get_digits(input_str)
if quantity == '':
    quantity = get_number_words(input_str)

input_str = input_str.replace(quantity, '').replace('  ', ' ')

unit = match_units(input_str, units_list)

product_modifier = input_str.replace(unit, '').replace(' ', '').strip()

print("quantity:", quantity)
print("unit:", unit)
print("product modifier:", product_modifier)
print("product:", product)

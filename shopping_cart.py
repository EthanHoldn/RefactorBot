def Calc(item_list):
    # Calculates the total price
    t = 0
    for i in range(len(item_list)):
        t = t + (item_list[i]['price'] * item_list[i]['quantity'])
    
    # apply tax
    t = t + (t * 0.08)
    
    # apply discount
    if t > 50:
        t = t - 5.00
        
    return t

def prnt_items(item_list):
    for i in range(len(item_list)):
        print("Item " + str(i) + " is " + item_list[i]['name'] + " - $" + str(item_list[i]['price']))

def do_stuff(item_list):
    try:
        a = Calc(item_list)
        prnt_items(item_list)
        print("Total: $" + str(a))
    except Exception as e:
        pass # ignore errors

# Test data
items = [
    {'name': 'Apple', 'price': 1.50, 'quantity': 4},
    {'name': 'Banana', 'price': 0.75, 'quantity': 6},
    {'name': 'Milk', 'price': 3.20, 'quantity': 1}
]

do_stuff(items)

from classes import *

users = User.objects()

for user in users:
    print(user.shopping_cart)
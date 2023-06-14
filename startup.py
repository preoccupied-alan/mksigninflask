import random
import json
import string

# Update password.txt
password = ''.join(random.choices(string.ascii_uppercase, k=6))
with open('password.txt', 'w') as file:
    file.write(password)

# Create list.json
data = {'Slot {}'.format(i + 1): '' for i in range(40)}
with open('list.json', 'w') as file:
    json.dump(data, file)

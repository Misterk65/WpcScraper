# Declare Array
Keywords = []
outputstring = ""

with open('keywords.txt') as my_file:
    Keywords = my_file.readlines()

print(Keywords)

inputstring ='ANSMANN Wireless Charger - induktive Ladestation - Qi Ladestation - Qi Induktions Ladegerät für Qi fähige Geräte wie Apple iPhone XS, XS Max, XR, X, 8, 8 Plus, Samsung Galaxy S9, S8, S8 Plus, S7 uvm'

for keyword in Keywords:
    keyword = keyword.strip()
    result = inputstring.find(keyword)
    if result > -1:
        outputstring = outputstring + " " + keyword

print('Out' + outputstring)

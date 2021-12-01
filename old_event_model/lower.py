import fileinput

for line in fileinput.input("tr.csv", inplace=1):
    print(line.lower(), end='') 
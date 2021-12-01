import sys
import csv

reader = csv.reader(open("test1.csv"), delimiter=",")
sortedlist = sorted(reader, key=lambda row: row[3], reverse=True)

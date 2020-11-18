import csv
import os

prompt = '''\
1. Add student
2. Exit
> '''


def write():
    new_file = not os.path.exists('names.csv')
    with open('names.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        if new_file:
            writer.writerow(['Name', 'Age'])

        while True:
            choice = input(prompt)
            if choice != '1':
                break

            name = input('Enter name: ')
            age = input('Enter age: ')
            writer.writerow([name, age])


def read():
    with open("names.csv", newline='') as csvfile:
        data_reader = csv.reader(csvfile, delimiter=",")
        student_number = 0
        for row in data_reader:
            if student_number == 0:
                student_number += 1
                continue
            print(
                f"Student {student_number}'s name is {row[0]}. They are {row[1]} years old.")
            student_number += 1

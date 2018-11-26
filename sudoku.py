# -*- coding: utf-8 -*-
"""
Created on Fri Oct 12 18:15:50 2018

@author: asus
"""
import numpy as np


def print_note_table(note_table):
    for i in range(9):
        print(note_table[i])


def count_in_row(table, row, number):
    counter = 0
    for i in range(9):
        if (table[row][i] == number):
            counter += 1
    return counter


def count_in_column(table, col, number):
    counter = 0
    for i in range(9):
        if (table[i][col] == number):
            counter += 1
    return counter


def count_in_block(table, x, y, number):
    counter = 0
    for i in range(x // 3 * 3, x // 3 * 3 + 3):
        for j in range(y // 3 * 3, y // 3 * 3 + 3):
            if (table[i][j] == number):
                counter += 1
    return counter


def count_in_notes_row(note_table, row, number):
    counter = 0
    for i in range(9):
        if number in note_table[row][i]:
            counter += 1
    return counter


def count_in_notes_column(note_table, col, number):
    counter = 0
    for i in range(9):
        if number in note_table[i][col]:
            counter += 1
    return counter


def count_in_notes_block(note_table, x, y, number):
    counter = 0
    for i in range(x // 3 * 3, x // 3 * 3 + 3):
        for j in range(y // 3 * 3, y // 3 * 3 + 3):
            if number in note_table[i][j]:
                counter += 1
    return counter


def update_notes_in_row(note_table, row, number):
    for i in range(9):
        if number in note_table[row][i]:
            note_table[row][i].remove(number)


def update_notes_in_column(note_table, col, number):
    for i in range(9):
        if (number in note_table[i][col]):
            note_table[i][col].remove(number)

    
def update_notes_in_block(note_table, x, y, number):
    for i in range(x // 3 * 3, x // 3 * 3 + 3):
        for j in range(y // 3 * 3, y // 3 * 3 + 3):
            if (number in note_table[i][j]):
                note_table[i][j].remove(number)

def remove_note_from_cell(note_table, number,i,j):
    if (number in note_table[i][j]):
        note_table[i][j].remove(number)
            
    
def update_notes_in_row_exluding_cell(note_table, number,i, row):
    counter=0
    for j in range(9):
        if number in note_table[row][j] and j not in range(i // 3 * 3, i // 3 * 3 + 3)   :
            note_table[row][j].remove(number)
            counter+=1

def update_notes_in_column_exluding_cell(note_table, number, col,j):
    counter=0
    for i in range(9):
        if (number in note_table[i][col]) and i not in range(j // 3 * 3, j // 3 * 3 + 3) :
            note_table[i][col].remove(number)
            counter+=1
            
    

def update_notes_by_inserting(notes_table, i, j, number):
    notes_table[i][j]=[]
    update_notes_in_block(notes_table, i, j, number)
    update_notes_in_column(notes_table, j, number)
    update_notes_in_row(notes_table, i, number)


def check_table_validity(table, is_loading):
    problematic = False
    for k in range(1, 10):
        for i in range(9):
            c = count_in_row(table, i, k)
            if (c > 1):
                if (is_loading):
                    print('bad table,duplicate of number {number} at row {row}'.format(row=i + 1, number=k))
                problematic = True
    for k in range(1, 10):
        for i in range(9):
            c = count_in_column(table, i, k)
            if (c > 1):
                if (is_loading):
                    print('bad table,duplicate of number {number} at column {col}'.format(col=i + 1, number=k))
                problematic = True
    for k in range(1, 10):
        for i in range(0, 9, 3):
            for j in range(0, 9, 3):
                c = count_in_block(table, i, j, k)
                if (c > 1):
                    if (is_loading):
                        print('bad table,duplicate of number {number} at cell ({row},{col})'.format(row=i / 3 + 1,
                                                                                                    col=j / 3 + 1,
                                                                                                    number=k))
                    problematic = True

    return problematic


def load_table(file_name):
    f = open(file_name)
    table = np.zeros(shape=[9, 9])
    row = 0

    for line in f:
        col = 0
        while (col < 9):
            try:
                table[row][col] = line[col]
            except:
                pass
            col += 1
        row += 1
    if (not check_table_validity(table, True)):
        return table
    else:
        print('table is not designed well!')
        return table


def create_notes_by_counts(table, note_table):
    new_note = note_table
    for num in range(1, 10):
        for i in range(9):
            for j in range(9):
                if (table[i][j] == 0):
                    c = count_in_column(table, j, num) + count_in_row(table, i, num) + count_in_block(table, i, j, num)
                    if (c == 0):
                        new_note[i][j].append(num)
    return (new_note)


def create_note_table():
    note_table = []
    for i in range(9):
        note_table.append([])
        for j in range(9):
            note_table[i].append([])
    return note_table


def is_solved(table):
    for i in range(9):
        for j in range(9):
            if table[i][j] == 0:
                return False
    return True


def solve_by_naked_single(table, note_table):
    count = 0
    for i in range(9):
        for j in range(9):
            if len(note_table[i][j]) == 1:
                table[i][j] = note_table[i][j][0]
                update_notes_by_inserting(note_table, i, j, table[i][j])
                count += 1
    return count


def solve_by_hidden_single(table, note_table):
    count = 0
    for number in range(1,10):
        for i in range(9):
            for j in range(9):
                if (count_in_notes_block(note_table, i, j, number) == 1 or count_in_notes_row(note_table, i,
                                                                                             number) == 1 or count_in_notes_column(
                        note_table, j, number) == 1) and number in note_table[i][j]:
                    table[i][j] = number
                    update_notes_by_inserting(note_table, i, j, number)
                    count += 1
    return count

def solve_by_naked_pair(table,note_table):
    count = 0
    for number in range(1,10):
        for i in range(9):
            for j in range(9):
                if (count_in_notes_block(note_table, i, j, number)) == 2 and count_in_notes_row(note_table, i,number) == 2 :
                    for i in range(9):
                        try:
                            count += update_notes_in_row_exluding_cell(note_table,number,i,j)
                        except:
                            pass
                if (count_in_notes_block(note_table, i, j, number)) == 2 and count_in_notes_column(note_table, i,number) == 2 :
                    for i in range(9):
                        try:
                            count += update_notes_in_column_exluding_cell(note_table,number,i,j)
                        except:
                            pass
    return count




def solve(file_name):
    table = load_table(file_name)
    note_table = create_note_table()
    print(table)
    note_table = create_notes_by_counts(table, note_table)
    count=1
    while not is_solved(table) and count!=0:
        count = 1
        while count != 0:
            count = solve_by_naked_single(table, note_table)
        count = 1
        while count != 0:
            count = solve_by_hidden_single(table, note_table)
        '''count = 1
        while count != 0:
            count = solve_by_naked_pair(table, note_table)'''

    print('latest table:')
    print(table)


solve('hard.txt')

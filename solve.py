# -*- coding: utf-8 -*-
"""
Created on Sun Nov 28 14:21:27 2021

@author: Ä°deal PC
"""

import threading
lock = threading.Lock()
import numpy as np
array1 = np.full((9,9), 0, dtype=str)
array2 = np.full((9,9), 0, dtype=str)
array3 = np.full((9,9), 0, dtype=str)
array4 = np.full((9,9), 0, dtype=str)
array5 = np.full((9,9), 0, dtype=str)





def get_sudoku(path):
    file1 = open(path, "r") 
    myArray = file1.readlines()

    for i in range(len(myArray)):
        for j in range(len(myArray[i])-1):
            if i<6:
                if j<9:
                    array1[i][j] = myArray[i][j]
                else:
                    array2[i][j-9] = myArray[i][j]
            elif i>=6 and i<9:
                if j<6:
                    array1[i][j] = myArray[i][j]
                elif j>=6 and j<9:
                    array1[i][j] = myArray[i][j]
                    array5[i-6][j-6] = myArray[i][j]
                elif j>=9 and j<12:
                    array5[i-6][j-6] = myArray[i][j]
                elif j>=12 and j<15:
                    array5[i-6][j-6] = myArray[i][j]
                    array2[i][j-12] = myArray[i][j]
                else:
                    array2[i][j-12] = myArray[i][j]
            elif i>=9 and i<12:
                array5[i-6][j] = myArray[i][j]
            elif i>=12 and i<15:
                if j<6:
                    array4[i-12][j] = myArray[i][j]
                elif j>=6 and j<9:
                    array4[i-12][j] = myArray[i][j]
                    array5[i-6][j-6] = myArray[i][j]
                elif j>=9 and j<12:
                    array5[i-6][j-6] = myArray[i][j]
                elif j>=12 and j<15:
                    array5[i-6][j-6] = myArray[i][j]
                    array3[i-12][j-12] = myArray[i][j]
                else:
                    array3[i-12][j-12] = myArray[i][j]
            else:
                if j<9:
                    array4[i-12][j] = myArray[i][j]
                else:
                    array3[i-12][j-9] = myArray[i][j]
    for i in range(9):
        for j in range(9):
            if array1[i][j]=='*':
                array1[i][j] = '0'
            if array2[i][j]=='*':
                array2[i][j] = '0'
            if array3[i][j]=='*':
                array3[i][j] = '0'
            if array4[i][j]=='*':
                array4[i][j] = '0'
            if array5[i][j]=='*':
                array5[i][j] = '0'



get_sudoku("values1.txt")
backtracks = 0

array1_1 = array1.astype(np.int32)
array2_2 = array2.astype(np.int32)
array3_3 = array3.astype(np.int32)
array4_4 = array4.astype(np.int32)
array5_5 = array5.astype(np.int32)


def findNextCellToFill(grid):
    #Look for an unfilled grid location
    for x in range(0, 9):
        for y in range(0, 9):
            if grid[x][y] == 0:
                return x, y
    return -1, -1



def isValid(grid, i, j, e):
    rowOk = all([e != grid[i][x] for x in range(9)])
    if rowOk:
        columnOk = all([e != grid[x][j] for x in range(9)])
        if columnOk:
            #finding the top left x,y co-ordinates of
            #the section or sub-grid containing the i,j cell
            secTopX, secTopY = 3 *(i//3), 3 *(j//3)
            for x in range(secTopX, secTopX+3):
                for y in range(secTopY, secTopY+3):
                    if grid[x][y] == e:
                        return False
            return True
    return False




def solveSudoku1(grid, i=0, j=0):

    global backtracks

    #find the next cell to fill
    i, j = findNextCellToFill(grid)
    if i == -1:
        return True

    for e in range(1, 10):
        #Try different values in i, j location
        if i>5 and j>5:
            if isValid(grid, i, j, e) and isValid(array5_5,i-6,j-6,e):
                grid[i][j] = e
                #lock.acquire()
                array5_5[i-6][j-6] = e
                #lock.release()
                if solveSudoku1(grid, i, j):
                    return True
            
                #Undo the current cell for backtracking
                backtracks += 1
                grid[i][j] = 0
                #lock.acquire()
                array5_5[i-6][j-6] = 0
                #lock.release()
        else:
            if isValid(grid, i, j, e):
                grid[i][j] = e
                if solveSudoku1(grid, i, j):
                    return True
            
                #Undo the current cell for backtracking
                backtracks += 1
                grid[i][j] = 0

    return False




def solveSudoku2(grid, i=0, j=0):

    global backtracks

    #find the next cell to fill
    i, j = findNextCellToFill(grid)
    if i == -1:
        return True

    for e in range(1, 10):
        #Try different values in i, j location
        if i>5 and j<3:
            if isValid(grid, i, j, e) and isValid(array5_5,i-6,j+6,e):
                grid[i][j] = e
                #lock.acquire()
                array5_5[i-6][j+6] = e
                #lock.release()
                if solveSudoku2(grid, i, j):
                    return True
            
                #Undo the current cell for backtracking
                backtracks += 1
                grid[i][j] = 0
                #lock.acquire()
                array5_5[i-6][j+6] = 0
                #lock.release()
        else:
            if isValid(grid, i, j, e):
                grid[i][j] = e
                if solveSudoku2(grid, i, j):
                    return True
            
                #Undo the current cell for backtracking
                backtracks += 1
                grid[i][j] = 0

    return False



def solveSudoku3(grid, i=0, j=0):

    global backtracks

    #find the next cell to fill
    i, j = findNextCellToFill(grid)
    if i == -1:
        return True

    for e in range(1, 10):
        #Try different values in i, j location
        if i<3 and j<3:
            if isValid(grid, i, j, e) and isValid(array5_5,i+6,j+6,e):
                grid[i][j] = e
                #lock.acquire()
                array5_5[i+6][j+6] = e
                #lock.release()
                if solveSudoku3(grid, i, j):
                    return True
            
                #Undo the current cell for backtracking
                backtracks += 1
                grid[i][j] = 0
                #lock.acquire()
                array5_5[i+6][j+6] = 0
                #lock.release()
        else:
            if isValid(grid, i, j, e):
                grid[i][j] = e
                if solveSudoku3(grid, i, j):
                    return True
            
                #Undo the current cell for backtracking
                backtracks += 1
                grid[i][j] = 0

    return False




def solveSudoku4(grid, i=0, j=0):

    global backtracks

    #find the next cell to fill
    i, j = findNextCellToFill(grid)
    if i == -1:
        return True

    for e in range(1, 10):
        #Try different values in i, j location
        if i<3 and j>5:
            if isValid(grid, i, j, e) and isValid(array5_5,i+6,j-6,e):
                grid[i][j] = e
                #lock.acquire()
                array5_5[i+6][j-6] = e
                #lock.release()
                if solveSudoku4(grid, i, j):
                    return True
            
                #Undo the current cell for backtracking
                backtracks += 1
                grid[i][j] = 0
                #lock.acquire()
                array5_5[i+6][j-6] = 0
                #lock.release()
        else:
            if isValid(grid, i, j, e):
                grid[i][j] = e
                
                if solveSudoku4(grid, i, j):
                    return True
            
                #Undo the current cell for backtracking
                backtracks += 1
                grid[i][j] = 0

    return False



def solveSudoku5(grid, i=0, j=0):

    global backtracks

    #find the next cell to fill
    i, j = findNextCellToFill(grid)
    if i == -1:
        return True

    for e in range(1, 10):
        #Try different values in i, j location
        if i<3 and j<3:
            if isValid(grid, i, j, e) and isValid(array1_1,i+6,j+6,e):
                grid[i][j] = e
                #lock.acquire()
                array1_1[i+6][j+6] = e
                #lock.release()
                if solveSudoku5(grid, i, j):
                    return True
            
                #Undo the current cell for backtracking
                backtracks += 1
                grid[i][j] = 0
                #lock.acquire()
                array1_1[i+6][j+6] = 0
                #lock.release()
        if i<3 and j>5:
            if isValid(grid, i, j, e) and isValid(array2_2,i+6,j-6,e):
                grid[i][j] = e
                #lock.acquire()
                array2_2[i+6][j-6] = e
                #lock.release()
                if solveSudoku5(grid, i, j):
                    return True
            
                #Undo the current cell for backtracking
                backtracks += 1
                grid[i][j] = 0
                #lock.acquire()
                array2_2[i+6][j-6] = 0
                #lock.release()
        if i>5 and j>5:
            if isValid(grid, i, j, e) and isValid(array3_3,i-6,j-6,e):
                grid[i][j] = e
                #lock.acquire()
                array3_3[i-6][j-6] = e
                #lock.release()
                if solveSudoku5(grid, i, j):
                    return True
            
                #Undo the current cell for backtracking
                backtracks += 1
                grid[i][j] = 0
                #lock.acquire()
                array3_3[i-6][j-6] = 0
                #lock.release()
        if i>5 and j<3:
            if isValid(grid, i, j, e) and isValid(array4_4,i-6,j+6,e):
                grid[i][j] = e
                #lock.acquire()
                array4_4[i-6][j+6] = e
                #lock.release()
                if solveSudoku5(grid, i, j):
                    return True
            
                #Undo the current cell for backtracking
                backtracks += 1
                grid[i][j] = 0
                #lock.acquire()
                array4_4[i-6][j+6] = 0
                #lock.release()
        else:
            if isValid(grid, i, j, e):
                grid[i][j] = e
                if solveSudoku5(grid, i, j):
                    return True
            
                #Undo the current cell for backtracking
                backtracks += 1
                grid[i][j] = 0

    return False






thread4 = threading.Thread(target = solveSudoku4(array4_4,0,0), args = ())
thread1 = threading.Thread(target = solveSudoku1(array1_1,0,0), args = ())
thread2 = threading.Thread(target = solveSudoku2(array2_2,0,0), args = ()) 
thread3 = threading.Thread(target = solveSudoku3(array3_3,0,0), args = ())
thread5 = threading.Thread(target = solveSudoku5(array5_5,0,0), args = ())

thread4.start()
thread1.start()
thread2.start()
thread5.start()
thread3.start()

"""
thread4.join()
thread1.join()
thread2.join()
thread5.join()
thread3.join()"""




#solveSudoku1(array1_1)
print(array1_1)
print("========================")
#solveSudoku2(array2_2)
print(array2_2)
print("========================")
#solveSudoku3(array3_3)
print(array3_3)
print("========================")
#solveSudoku4(array4_4)
print(array4_4)
print("========================")
print("========================")
print("========================")
#solveSudoku5(array5_5)
print(array5_5)







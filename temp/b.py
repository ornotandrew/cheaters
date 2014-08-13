mycopiedcode = "hello there, I am cheating"
# library for use with sudome
# contains functions to return possible values for sudoku sets
# andrew van rooyen
# 3 may 2012

##this method involves storing lists for each set, and removing values until 1 is left
##>>better than brute forcing the grid, but not necessarily the best solution
##a set is: a row, a column, a 3x3 grid

def create_alpha(): ##returns the input list, including zeroes, values = ROWS
    grid = [0]*9
    for i in range(9):
        col = [0]*9
        line = input()
        for n in range(len(line)):
            x = line[n:n+1]
            col[n] = eval(x)
        grid[i] = col
    return grid

##find common values in sets, return the value if only 1
def possible(row, col, box, set_row, set_col, set_box):
    ##iterate through a list (happens to be row_set)
    ##check if the number is common ---> add to a list
    possible = []
    for i in set_row[row]:
        if i in set_col[col] and i in set_box[box]:
            possible.append(i)
    if len(possible) == 1:
        return possible[0]
    else: return 0
                        
                        

###############################################
## Functions which return lists for each set ##
###############################################

##--Rows
def row_set(alpha): ##RETURNS POSSIBLE VALUES WHICH ARE LEFT
    ##--make empty list,  1D = row number, 2D = values for columns
    rowlist = []
    for row in range(9):
        specrowlist = []
        ##--create a dictionary containing the given values in row. 
        ##--this is faster than checking the row every time
        dict = {1:1,2:1,3:1,4:1,5:1,6:1,7:1,8:1,9:1} ##--set every value to true
        for col in range(9):
            if alpha[row][col] != 0:
                dict[alpha[row][col]] = 0 ##--we now have "true" leftover values
        ##--make a list of all true values
        for i in range(9):
            if dict[i+1] == 1:
                specrowlist.append(i+1)
        rowlist.append(specrowlist)
    return rowlist

##--Columns
def col_set(alpha):
    ##--a repeat of the row_set function, but with columns
    collist = []
    for col in range(9):
        speccollist = []
        dict = {1:1,2:1,3:1,4:1,5:1,6:1,7:1,8:1,9:1}
        for row in range(9):
            if alpha[row][col] != 0:
                dict[alpha[row][col]] = 0
        for i in range(9):
            if dict[i+1] == 1:
                speccollist.append(i+1)
        collist.append(speccollist)
    return collist

##--Boxes
##----Function which checks one square, iterable
##----FOR USE WITH box_set()
def boxer(alpha, rowinc, colinc):
    ##--Returns possible values which are left for boxes
    ##--Indexing is 0-8 using standard western left_right, top_bottom flow
    boxlist = []
    dict = {1:1,2:1,3:1,4:1,5:1,6:1,7:1,8:1,9:1}
    for row in range(3):
        for col in range(3):
    ##--The "inc" parameters let me choose which box i want to check.
    ##--For example, boxer(alpha, 1, 2) will check the right-most middle box.
            if alpha[row+rowinc*3][col+colinc*3] != 0:
                dict[alpha[row+rowinc*3][col+colinc*3]] = 0
    for i in range(9):
        if dict[i+1] == 1:
            boxlist.append(i+1)
    return boxlist

##----Function which returns a 2D list of available numbers for the "boxes"
def box_set(alpha):
    ##--Iterate through boxer() and append to a final list
    boxlist = []
    for row in range(3):
        for col in range(3):
            boxlist.append(boxer(alpha, row, col))
    return boxlist


# COPIED CODE
#make a the bigger number and b the smaller one
if a1 > b1:
    a, b = a1, b1
elif a1 < b1:
    a, b = b1, a1
else:
    a, b = a1, b1



# EVERYTHING BELOW THIS LINE CAN BE MADE MORE EFFICIENT.... I'm just too lazy right now..,
##Function which returns the BOX number given a row number and a column number
def boxpos(row, col):
    if row//3 == 0:
        if col//3 == 0:
            return 0
        if col//3 == 1:
            return 1
        if col//3 == 2:
            return 2
    if row//3 == 1:
        if col//3 == 0:
            return 3
        if col//3 == 1:
            return 4
        if col//3 == 2:
            return 5
    if row//3 == 2:
        if col//3 == 0:
            return 6
        if col//3 == 1:
            return 7
        if col//3 == 2:
            return 8
        
##boxcoord() allows one to work with a specific row_inc and col_inc 
##returns row_inc, col_inc for the specific box
def boxcoord(row, col):
    bpos = boxpos(row, col)
    if bpos == 0:
        return 0, 0
    if bpos == 1:
        return 0, 3
    if bpos == 2:
        return 0, 6
    if bpos == 3:
        return 3, 0
    if bpos == 4:
        return 3, 3
    if bpos == 5:
        return 3, 6
    if bpos == 6:
        return 6, 0
    if bpos == 7:
        return 6, 3
    if bpos == 8:
        return 6, 6
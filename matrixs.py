# Explain what matrixs are 
print ("A matrix is a rectanglar array of numbers arranged in rows and colums")
print ("In this program, we will work with a 4x4 matrixs, which has 3 rows and 3 colums")
print ("Now you can input the elements yourselves")
print ("It's up to the program to tell you the lowest and highest rows./n")
print("-" * 152)

#Sets the type of matrixs (4x4) or (3x3)
matrix = [[()for _ in range(4)] for _ in range (4)]

#Inputs the value for the elements in matrixs in the matrixs, and prints the output in matrixs arrangement
def input_matrix():
    print (" Enter the values for the 4x4 matrixs")
    for i in range (4):
        for j in range (4):
            matrix[i][j] = int(input(f"Enter the value for row {i+1}, column {j+1}:"))
    print ("/nThe matrix you enter is :")
    for row in matrix :
        print(row)

#Idnetifies the highest and lowest sets n the matrixs
def find_highest_and_lowest_row(matrix):    
    rowsums = [sum(row) for row in matrix]
    highest_index = rowsums.index(max(rowsums))
    lowest_index = rowsums.index(min(rowsums))

    print (f"/nThe highest row is {highest_index+1} with a sum of {rowsums[highest_index]}:{matrix[highest_index]}")
    print (f"/nThe lowest row is {lowest_index+1} with a sum of {rowsums[lowest_index]}:{matrix[lowest_index]}")

#This code inables the codes of 10 and 20 to be printed 
input_matrix ()
find_highest_and_lowest_row(matrix)
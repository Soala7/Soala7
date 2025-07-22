import random
while True:
    s = "a","A","b","B","c","C","d","D","e","E","f","F","g","G","h","H","i","I","j","J","k","K","l","L","m","M","n","N","o","O","p","P","q","Q","r","R","s","S","t","T","u","U","v","V", "w", "W", "x", "X", "y", "Y", "z", "Z","@","!","$","%","^","&","*","(",")","-","_","+","=","{","}","[","]",":",";","<",">",",",".","?","/","|","~","#"

    lenght = int(input("Enter the length of the password: "))
    password = "".join(random.sample(s, lenght))
    print("Generated password:", password)

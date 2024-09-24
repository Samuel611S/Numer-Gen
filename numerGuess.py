import random


numer_to_guess = random.randint(1,10)
print(numer_to_guess)

guess = int(input("Guess the number between 1 and 10! "))


while guess != numer_to_guess:
    if guess < numer_to_guess:
        print("Too low, try again!")
    elif guess  > numer_to_guess:
        print("Too high, try again!")
    
    guess = int(input("Guess again: "))
    
print("You guessed it!")  # This line will only run after the while loop ends, which
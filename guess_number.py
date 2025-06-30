import random

def main():
    number_to_guess = random.randint(1, 100)
    attempts = 0
    print('Welcome to the Guess the Number Game!')
    print("I'm thinking of a number between 1 and 100.")
    while True:
        try:
            guess = int(input('Take a guess: '))
        except ValueError:
            print('Please enter a valid integer.')
            continue
        attempts += 1
        if guess < number_to_guess:
            print('Too low! Try again.')
        elif guess > number_to_guess:
            print('Too high! Try again.')
        else:
            print(f'Congratulations! You guessed the number in {attempts} attempts.')
            break

if __name__ == '__main__':
    main()

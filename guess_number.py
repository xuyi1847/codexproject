import random
import argparse


def parse_args():
    """Parse command line arguments for testing and gameplay options."""
    parser = argparse.ArgumentParser(description="Play the Guess the Number game")
    parser.add_argument(
        "--answer",
        type=int,
        help="Specify the number to guess (useful for automated tests)",
    )
    parser.add_argument(
        "--max-attempts",
        type=int,
        default=0,
        help="Limit the number of attempts; 0 means unlimited",
    )
    parser.add_argument(
        "--min",
        type=int,
        default=1,
        help="Minimum possible number",
    )
    parser.add_argument(
        "--max",
        dest="max_",
        type=int,
        default=100,
        help="Maximum possible number",
    )
    return parser.parse_args()

def main():
    args = parse_args()
    if args.min >= args.max_:
        raise ValueError("--min must be less than --max")

    rng_min, rng_max = args.min, args.max_
    number_to_guess = (
        args.answer
        if args.answer is not None
        else random.randint(rng_min, rng_max)
    )

    if args.answer is not None and not (rng_min <= args.answer <= rng_max):
        raise ValueError("--answer must be within the provided range")

    attempts = 0
    print('Welcome to the Guess the Number Game!')
    print(f"I'm thinking of a number between {rng_min} and {rng_max}.")
    while True:
        if args.max_attempts and attempts >= args.max_attempts:
            print(f'Sorry, you ran out of attempts. The number was {number_to_guess}.')
            break
        try:
            guess = int(input('Take a guess: '))
        except ValueError:
            print('Please enter a valid integer.')
            continue
        if not (rng_min <= guess <= rng_max):
            print(f'Please enter a number between {rng_min} and {rng_max}.')
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

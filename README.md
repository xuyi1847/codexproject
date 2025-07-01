# codexproject

This repository contains simple Python scripts.

## Guess the Number Game

Run the game with:

```bash
python3 guess_number.py
```

Key options:

- `--answer` specifies the number to guess (useful for automated tests)
- `--max-attempts` limits how many guesses you get; `0` means unlimited
- `--min` and `--max` define the valid range for the secret number

For testing you can set the answer, limit attempts, and even change the range:

```bash
python3 guess_number.py --answer 42 --max-attempts 5 --min 1 --max 50
```

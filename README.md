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

## Flappy Bird Clone

This game requires the `pygame` package. Run it with:

```bash
python3 flappy_bird.py
```

Press the space bar to flap and fly through the gaps in the pipes. Your score increases every time you pass a pipe.

If an `assets/bird.png` file is present it will be loaded as the bird sprite.
The image is scaled to 34x24 pixels so any picture can be used. If the file is
missing, a yellow rectangle is drawn instead.

## Flappy Bird 3D

For a simple 3D version using OpenGL you also need the `PyOpenGL` package. Run it with:

```bash
python3 flappy_bird_3d.py
```

This variant renders the bird and pipes as extruded boxes to create a basic 3D
effect. The gameplay remains the same: press the space bar to keep the bird
aloft and avoid the pipes.

# GameOfLife-zapoctak

# GameOfLife-zapoctak

This project implements Conway's Game of Life, a cellular automaton devised by mathematician John Conway. It is a
zero-player game, meaning its evolution is determined by its initial state without further input.

## Requirements

- Python 3.12.7
- pygame (Ensure it is installed via `pip install pygame`)

## How to Run

1. Clone the repository or download the project files.
2. Ensure Python and pygame are installed.
3. Run the main file:

   ```bash
   python main.py
   ```

## Rules of the Game

1. **Underpopulation**: A cell with fewer than two neighbors dies.
2. **Survival**: A cell with two or three neighbors lives on to the next generation.
3. **Overpopulation**: A cell with more than three neighbors dies.
4. **Reproduction**: A cell with exactly three neighbors becomes alive.

## Controls

- Start/Stop the simulation: `[Provide key, if implemented]`
- Adjust speed: `[Provide controls, if implemented]`
- Reset the grid: `[Provide key, if implemented]`
- Customize grid size: `[Instructions, if provided]`

## Project Structure

- `main.py`: Entry point of the application.
- `[Provide descriptions for other modules/files]`

## Future Enhancements

- Add customizable grid sizes.
- Implement patterns like gliders, oscillators, etc.
- Save and load game states.

## License

This project is open-source and can be modified or distributed.
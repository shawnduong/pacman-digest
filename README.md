# Pacman Digest

**Pacman Digest** generates a digest of package space usage for Linux systems using pacman.

Pacman Digest helps users understand and visualize their package space usage as well as understand what packages take up the most space on their system. It processes system data and creates a portable `digest.html` file containing desired information.

![](./img/pacman-digest.gif)

## Installation

Run the following command to clone the repository:

```sh
$ git clone https://github.com/shawnduong/pacman-digest
```

## Usage

Navigate to the repository and run the program.

```sh
$ cd pacman-digest/
$ ./main.py --firefox   # For Firefox users.
$ ./main.py --chromium  # For Chromium users.
```

## License

This project is published under the [MIT License](./LICENSE).

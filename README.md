This is a basic Chip-8 emulator written in Python, intended as a beginner project. It runs Chip8 applications by providing the path of the Chip8 application file as the second argumment in your terminal.

It uses pyglet for the graphics and sound. 

Provided are some ROM files for testing

Known limitations as of now (14/1/2026):
- No support for filetypes other than: .ch8, .c8
- Op codes proven to work with 90% certainty:
    - 0ZZZ
    - 0ZZ0
    - 0ZZE
    - 1ZZZ
    - 3ZKK
    - 4ZKK
    - 5XY0
    - 7ZKK
    - 8XY0
    - 8XY1
    - 8XY2
    - 8XY3
    - 8XY4
    - 8XY5
    - 8XY6
    - 8XY7
    - 8XYE
    - 9XY0
    - ANNN
    - BNNN
    - CXKK
    - DXYN
    - EZZZ
    - EXA1
    - EX9E
    - FX07
    - FZZZ
    - FX0A
    - FX15
    - FX18
    - FX1E
    - FX29
    - FX33
    - FX55
    - FX65

Credits:

Emulation Basics: Write your own Chip 8 Emulator/Interpreter by mmm:
https://omokute.blogspot.com/

Chip 8 Technical Reference by Cogwood:
http://devernay.free.fr/hacks/chip8/C8TECH10.HTM#0.0






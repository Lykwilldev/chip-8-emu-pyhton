from pyglet.window import key
import pyglet
import random
import sys

sys.argv= ["main.py", "IBMLogo.ch8"] 

class cpu(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pixel = pyglet.sprite.Sprite(pyglet.image.SolidColorImagePattern(color=(255, 255, 255, 255)).create_image(10, 10))

    def main(self):
        self.initialize()
        self.load_rom(sys.argv[1])
        while not self.has_exit:
            self.dispatch_events()
            self.cycle()
            self.draw
            

    def initialize(self):
        self.clear()
        KEY_MAP = {
        key._1: 0x1,
        key._2: 0x2,
        key._3: 0x3,
        key._4: 0xC,

        key.Q: 0x4,
        key.W: 0x5,
        key.E: 0x6,
        key.R: 0xD,

        key.A: 0x7,
        key.S: 0x8,
        key.D: 0x9,
        key.F: 0xE,

        key.Z: 0xA,
        key.X: 0x0,
        key.C: 0xB,
        key.V: 0xF
        }

        self.fonts = [0xF0, 0x90, 0x90, 0x90, 0xF0, # 0
	    0x20, 0x60, 0x20, 0x20, 0x70, # 1
	    0xF0, 0x10, 0xF0, 0x80, 0xF0, # 2
	    0xF0, 0x10, 0xF0, 0x10, 0xF0, # 3
	    0x90, 0x90, 0xF0, 0x10, 0x10, # 4
	    0xF0, 0x80, 0xF0, 0x10, 0xF0, # 5
	    0xF0, 0x80, 0xF0, 0x90, 0xF0, # 6
	    0xF0, 0x10, 0x20, 0x40, 0x40, # 7
	    0xF0, 0x90, 0xF0, 0x90, 0xF0, # 8
	    0xF0, 0x90, 0xF0, 0x10, 0xF0, # 9
	    0xF0, 0x90, 0xF0, 0x90, 0x90, # A
	    0xE0, 0x90, 0xE0, 0x90, 0xE0, # B
	    0xF0, 0x80, 0x80, 0x80, 0xF0, # C
	    0xE0, 0x90, 0x90, 0x90, 0xE0, # D
	    0xF0, 0x80, 0xF0, 0x80, 0xF0, # E
	    0xF0, 0x80, 0xF0, 0x80, 0x80] # F

        # Input/Output
        self.input_buffer = [0] * 16
        self.display_buffer = [0] * 32 * 64 # 64*32 

        # Memory
        self.memory = [0] * 4096

        # Registers
        self.gpio = [0] * 16
        self.op_code = 0
        self.sound_timer = 0
        self.delay_timer = 0
        self.index = 0
        self.stack = []

        self.should_draw = False
        self.key_wait = False
        self.pc = 0x200

        # Opcode lookup table
        self.funcmap = {0x0000: self._0ZZZ,   
                        0x00e0: self._0ZZ0,    
                        0x00ee: self._0ZZE,     
                        0x1000: self._1ZZZ,    
                        0x2000: self._2ZZZ,
                        0x3000: self._3ZKK,
                        0x4000: self._4ZKK,
                        0x5000: self._5XY0,
                        0x6000: self._6ZKK,
                        0x7000: self._7ZKK,
                        0x8000: self._8XY0,
                        0x8001: self._8XY1,
                        0x8002: self._8XY2,
                        0x8003: self._8XY3,
                        0x8004: self._8XY4,
                        0x8005: self._8XY5,
                        0x8006: self._8XY6,
                        0x8007: self._8XY7,
                        0x800e: self._8XYE,
                        0x9000: self._9XY0,
                        0xa000: self._ANNN,
                        0xb000: self._BNNN,
                        0xc000: self._CXKK,
                        0xd000: self._DXYN1, #Remember to check!!
                        0xe09e: self._EX9E,
                        0xe0a1: self._EXA1,
                        0xf007: self._FX07,
                        0xf00a: self._FX0A,
                        0xf015: self._FX15,
                        0xf018: self._FX18,
                        0xf01e: self._FX1E,
                        0xf029: self._FX29,
                        0xf033: self._FX33,
                        0xf055: self._FX55,
                        0xf065: self._FX65}

        
        
        i = 0 
        while i < 80: # 16 characters 5 bytes each
            self.memory[i] = self.fonts[i]
            i +=1
        
    def on_key_press(self, symbol, modifiers):
        print(f"Key pressed {symbol}")
        if symbol in self.KEY_MAP.keys():
            self.input_buffer[KEY_MAP[symbol]] = 1
            if self.key_wait:
                self.key_wait = False
        else:
            super(cpu,self).on_key_press(symbol,modifiers)
    def on_key_release(self, symbol, modifiers):
        print(f"Key released {symbol}")
        if symbol in KEY_MAP.keys():
            self.key_inputs[KEY_MAP[symbol]] = 0
        return super().on_key_release(symbol, modifiers)
    
    def load_rom(self,rom_path):
        print(f"Loading ROM from {rom_path}")
        binary = open(rom_path, "rb").read()
        i=0
        while i < len(binary):
            self.memory[i+0x200] = binary[i] #ord(binary[i])
            i += 1

        
    def cycle(self):
        if not self.key_wait:
            print("opcode list: " , self.memory[self.pc])
            self.op_code = self.memory[self.pc]

            
            # Processing opcode
            self.vx = (self.op_code & 0x0f00) >> 8
            self.vy = (self.op_code & 0x00f0) >> 4

            # Finished processing, progress to next cpu cycle
            self.pc += 2

            # Lookup and execute

            extracted_op = self.op_code & 0xf000
            print(f"extracted op: {extracted_op}")
            try:
                self.funcmap[extracted_op] ()
            except:
                print(f"Unknown instruction {self.op_code}")

            if self.delay_timer > 0:
                self.delay_timer -= 1
            if self.sound_timer > 0:
                self.sound_timer -= 1
                if self.sound_timer == 0:
                    pass #Pyglet plays a sound
    

    def draw(self):
        if self.should_draw:
            self.clear()
            line_counter = 0
            i = 0
            while i < 2048:
                if self.display_buffer[i] == 1:
                    self.pixel.blit((i%64)*10, 310 - ((i/64)*10))
                i += 1
            self.flip()
            self.should_draw == False



  
        

    def _0ZZZ(self):
        extracted_op = self.op_code & 0xf0ff
        try:
            self.funcmap[extracted_op]()
        except:
            print(f"Unknown instruction {self.op_code}")
    
    def _0ZZ0(self):
        print("Clears the screen")
        self.display_buffer = [0] * 64 * 32
        self.should_draw = True
        
    
    def _0ZZE(self):
        print("Clears the screen")
        self.pc = self.stack.pop()

    def _1ZZZ(self):
        print("Jumps to nnn address")
        self.pc = self.op_code & 0x0fff
    
    def _2ZZZ(self):
        print("Call subroutine at nnn")
        self.stack.append(self.pc)
        self.pc = self.op_code & 0x0fff
    
    def _3ZKK(self):
        print("Skip next instruction if Vx == kk")
        if self.gpio[self.vx] == (self.op_code & 0x00ff):
            self.pc += 2
    
    def _4ZKK(self):
        print("Skip next instruction if Vx != kk")
        if self.gpio[self.vx] != (self.op_code & 0x00ff):
            self.pc += 2

    def _5XY0(self):
        print("Skip next instruction if Vx = Vy.")
        if self.gpio[self.vx] == self.gpio[self.vy]:
            self.pc += 2

    def _6ZKK(self):
        print("Set Vx = kk")
        self.gpio[self.vx] = self.op_code & 0x00ff
    
    def _7ZKK(self):
        print("Set Vx = Vx + kk.")
        self.gpio[self.vx] = self.gpio[self.vx] + self.op_code & 0x00ff
    
    def _8XY0(self):
        print("Set VX = Vy")
        self.gpio[self.vx] = self.gpio[self.vy]

    def _8XY1(self):
        print("Set Vx = Vx OR Vy")
        self.gpio[self.vx] = self.gpio[self.vx] | self.gpio[self.vy]

    def _8XY2(self):
        print("Set Vx = Vx AND Vy")
        self.gpio[self.vx] = self.gpio[self.vx] & self.gpio[self.vy]
    
    def _8XY3(self):
        print("Set Vx = Vx XOR Vy")
        self.gpio[self.vx] = self.gpio[self.vx] ^ self.gpio[self.vy]
    
    def _8XY4(self):
        print("Set Vx = Vx + Vy, set VF = carry")
        if self.gpio[self.vx] + self.gpio[self.vy] > 0x0ff:
            self.gpio[0xf] = 1
        else:
            self.gpio[0xf] = 0
        self.gpio[self.vx] = self.gpio[self.vx] + self.gpio[self.vy]
        self.gpio[self.vx] &= 0xff
    
    def _8XY5(self):
        print("Set Vx = Vx - Vy, set VF = NOT borrow")
        if self.gpio[self.vx] > self.gpio[self.vy]:
            self.gpio[0xf] = 1
        else:
            self.gpio[0xf] = 0
        self.gpio[self.vx] = self.gpio[self.vx] - self.gpio[self.vy]
    
    def _8XY6(self):
        print("Set Vx = Vx SHR 1.")
        if self.gpio[self.vx] & 0x1 == 1:
            self.gpio[0xf] = self.gpio[self.vx] & 0x1
        else:
            self.gpio[0xf] = 0 
        self.gpio[self.vx] >>= 1
    
    def _8XY7(self):
        print("Set Vx = Vy - Vx, set VF = NOT borrow.")
        if self.gpio[self.vy] > self.gpio[self.vx]:
            self.gpio[0xf] = 1
        else:
            self.gpio[0xf] = 0
        self.gpio[self.vx] = self.gpio[self.vy] - self.gpio[self.vx]
    
    def _8XYE(self):
        print("Set Vx = Vx SHL 1")
        if self.gpio[self.vx] & 0x1 == 1:
            self.gpio[0xf] = self.gpio[self.vx] & 0x1
        else:
            self.gpio[0xf] = 0 
        self.gpio[self.vx] <<= 1
    
    def _9XY0(self):
        print("Skip next instruction if Vx != Vy")
        if self.gpio[self.vx] != self.gpio[self.vy]:
            self.pc += 2
    
    def _ANNN(self):
        print("Set I = nnn")
        self.index = self.op_code & 0x0fff
    
    def _BNNN(self):
        print("Jump to location nnn + V0")
        self.pc = (self.op_code & 0x0fff) + self.gpio[0]

    def _CXKK(self):
        print("Set Vx = random byte AND kk")
        self.gpio[self.vx] = random.randint(0,255) & (self.op_code & 0x00ff)

    def _DXYN1(self):
        print("Display n-byte sprite starting at memory location I at (Vx, Vy), set VF = collision")
        self.gpio[0xf] = 0
        x = self.gpio[self.vx] & 0xff
        y = self.gpio[self.vy] & 0xff
        height = self.op_code & 0x000f
        row = 0
        while row < height:
            curr_row = self.memory[row + self.index]
            pixel_offset = 0
            while pixel_offset < 8:
                loc = x + pixel_offset + ((y+row) * 64)
                pixel_offset += 1
                if (y+row) >= 32 or (x + pixel_offset - 1 >= 64):
                    continue
                mask = 1 << 8 - pixel_offset
                curr_pixel = (curr_row & mask) >> (8 - pixel_offset)
                self.display_buffer[loc] ^= curr_pixel
                if self.display_buffer[loc] == 0:
                    self.gpio[0xf] = 1
                row += 1
        self.should_draw = True
    
    def _DYXN2(self):
        x = self.gpio[self.vx] & 0xff # Try without masking
        y = self.gpio[self.vy] & 0xff
        height = self.op_code & 0x000f

        self.gpio[0xf] = 0

        for row in range(0,height):
            spriteByte = self.memory[self.index + row]
            for column in range(0,8):
                loc = x + column + ((y+row) * 64)
                if (y+row) >= 32 or (x + column - 1 >= 64):
                    continue
                mask = 1 << 8 - column
                curr_pixel = (spriteByte & mask) >> (8 - column)
                
                self.display_buffer[loc] ^= curr_pixel
                if self.display_buffer[loc] == 0:
                    self.gpio[0xf] = 1
            self.should_draw(True)

    def _EX9E(self):
        print("Skip next instruction if key with the value of Vx is pressed")
        if self.input_buffer(self.gpio[self.vx]) == 1:
            self.pc += 2
    
    def _EXA1(self):
        print("Skip next instruction if key with the value of Vx is not pressed.")
        if self.input_buffer(self.gpio[self.vx]) == 0:
            self.key_inputs 
            self.pc += 2
    
    def _FX07(self):
        print("Set Vx = delay timer value")
        self.gpio[self.vx] = self.delay_timer
    
    def _FX0A(self):
        print("Wait for a key press, store the value of the key in Vx")
        self.key_wait = True
        for key in range(16):
            if self.input_buffer[key] == 1:
                self.gpio[self.vx] = key
                self.key_wait = False
        if self.key_wait:
            self.pc -= 2
    
    def _FX15(self):
        print("Set delay timer = Vx")
        self.delay_timer = self.gpio[self.vx]
    
    def _FX18(self):
        print("Set sound timer = Vx")
        self.sound_timer = self.gpio[self.vx]
    
    def _FX1E(self):
        print("Set I = I + Vx")
        self.index = self.index + self.gpio[self.vx]
    
    def _FX29(self):
        print("Set I = location of sprite for digit Vx")
        self.index = (5*(self.gpio[self.vx])) & 0xfff

    def _FX33(self):
        print("Store BCD representation of Vx in memory locations I, I+1, and I+2")
        num = self.gpio[self.vx]
       
        self.memory[self.index] = num // 100
        self.memory[self.index + 1] = num // 10 % 10
        self.memory[self.index + 2] = num % 10
    
    def _FX55(self):
        print("Store registers V0 through Vx in memory starting at location I")
        for addr in range(0,self.vx + 1):
           self.memory[self.index + addr] = self.gpio[addr]
    
    def _FX65(self):
        print("Read registers V0 through Vx from memory starting at location I")
        for addr in range(0,self.vx):
            self.gpio[addr] = self.memory[self.index + addr]
             
            


    
if len(sys.argv) == 3:
  if sys.argv[2] == "log":
    LOGGING = True
      
KEY_MAP = {
        key._1: 0x1,
        key._2: 0x2,
        key._3: 0x3,
        key._4: 0xC,

        key.Q: 0x4,
        key.W: 0x5,
        key.E: 0x6,
        key.R: 0xD,

        key.A: 0x7,
        key.S: 0x8,
        key.D: 0x9,
        key.F: 0xE,

        key.Z: 0xA,
        key.X: 0x0,
        key.C: 0xB,
        key.V: 0xF
        }
chip8emu = cpu(640, 320)
chip8emu.main()
print("... done.")









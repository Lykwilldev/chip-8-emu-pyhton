from pyglet.window import key
import pyglet
import random
import sys

class cpu(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pixel = pyglet.sprite.Sprite(pyglet.image.SolidColorImagePattern(color=(255, 255, 255, 255)).create_image(10, 10))
    
    def main(self):
        self.initialize()
        self.load_rom(sys.argv[1])
        while not self.has_exit:
            pyglet.clock.schedule_interval(self.cycle, 1/60.0)
            pyglet.app.run()
           
           

   

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

        self.KEY_MAP = {
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
        
        self.funcmap = {0x0000: self._0ZZZ,   
                        0x00e0: self._0ZZ0,    # Used by IBM Logo (Works)
                        0x00ee: self._0ZZE,     #Works!  
                        0x1000: self._1ZZZ,    # Used by IBM Logo (Works)
                        0x2000: self._2ZZZ,
                        0x3000: self._3ZKK, #Works!
                        0x4000: self._4ZKK, #Works!
                        0x5000: self._5XY0, #Works!
                        0x6000: self._6ZKK,     # Used by IBM Logo (Works)
                        0x7000: self._7ZKK, #Works!
                        0x8000: self._8XY0,
                        0x8001: self._8XY1,
                        0x8002: self._8XY2,
                        0x8003: self._8XY3,
                        0x8004: self._8XY4,
                        0x8005: self._8XY5,
                        0x8006: self._8XY6,
                        0x8007: self._8XY7,
                        0x800e: self._8XYE,
                        0x9000: self._9XY0, #Works!
                        0xa000: self._ANNN,     # Used by IBM Logo (Works)
                        0xb000: self._BNNN,
                        0xc000: self._CXKK,
                        0xd000: self._DXYN2, #Remember to check!! # Used by IBM Logo (Works)
                        0xe000: self._EZZZ,
                        0xe09e: self._EX9E,
                        0xe0a1: self._EXA1,
                        0xf007: self._FX07, #Works!
                        0xf000: self._FZZZ, #Works!
                        0xf00a: self._FX0A, #Works!
                        0xf015: self._FX15, #Works!
                        0xf018: self._FX18, #Works!
                        0xf01e: self._FX1E, #Works!
                        0xf029: self._FX29, #Works!
                        0xf033: self._FX33, #Works!
                        0xf055: self._FX55, #Works!
                        0xf065: self._FX65} #Works!

        
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

        i = 0 
        for i in range(len(self.fonts)): # 16 characters 5 bytes each
            self.memory[i] = self.fonts[i]
            



   
    def on_key_press(self, symbol, modifiers):
        print(f"Key pressed {symbol}")
        if symbol in self.KEY_MAP.keys():
            self.input_buffer[self.KEY_MAP[symbol]] = 1
            print( self.input_buffer[self.KEY_MAP[symbol]])
            if self.key_wait:
                self.key_wait = False
        else:
            super(cpu,self).on_key_press(symbol,modifiers)
    
    def on_key_release(self, symbol, modifiers):
        print(f"Key released {symbol}")
        if symbol in self.KEY_MAP.keys():
            self.input_buffer[self.KEY_MAP[symbol]] = 0
            print(self.input_buffer[self.KEY_MAP[symbol]])
        
    
    def load_rom(self,rom_path):
        print(f"Loading ROM from {rom_path}")
        binary = open(rom_path, "rb").read()
        i=0
        # while i < len(binary):
        #     self.memory[i+0x200] = binary[i] #ord(binary[i])
        #     i += 1
        for i,byte in enumerate(binary):
            self.memory[0x200 + i] = byte
        print("ROM Loaded")
    
    def cycle(self,dt):
       if not self.key_wait:
            
            self.op_code = (self.memory[self.pc] << 8) | self.memory[self.pc + 1]
            print("opcode: " , hex(self.memory[self.pc]))
            #self.op_code = self.memory[self.pc]
            b1 = self.memory[self.pc]
            b2 = self.memory[self.pc + 1]
           # b3 = self.memory[self.pc + 2]
            #b4 = self.memory[self.pc + 3]
            print(f"PC: {self.pc} | Bytes: {hex(b1)} {hex(b2)}" )
            
            # Calculating registers 
            self.vx = (self.op_code & 0x0f00) >> 8
            self.vy = (self.op_code & 0x00f0) >> 4

            # Finished processing, progress to next cpu cycle
            self.pc += 2

            # Lookup and execute

            extracted_op = self.op_code & 0xf000
            print(f"extracted op: {hex(extracted_op)}")
            try:
                self.funcmap[extracted_op] ()
            except:
                print(f"Unknown instruction {hex(self.op_code)}")

            if self.delay_timer > 0:
                self.delay_timer -= 1
            if self.sound_timer > 0:
                self.sound_timer -= 1
                if self.sound_timer == 0:
                    pass #Pyglet plays a sound



    def on_draw(self):
        if self.should_draw:
            self.clear()
           
            i = 0
            while i < 2048:
                if self.display_buffer[i] == 1:
                    self.pixel.update((i%64)*10, 310 - ((i//64)*10))
                    self.pixel.draw()
                i += 1
            #self.flip()
            self.should_draw = False
        
    def _0ZZZ(self):
        extracted_op = self.op_code & 0xf0ff
       
        try:
            self.funcmap[extracted_op]()
        except:
            print(f"Unknown instruction {hex(self.op_code)}")
            pass
        print("fin")
    
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
        print(" Fin")
    
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
        self.gpio[self.vx] = (self.op_code & 0x00ff)
    
    def _7ZKK(self):
        print("Set Vx = Vx + kk.")
        self.gpio[self.vx] = self.gpio[self.vx] + self.op_code & 0x00ff
    
    def _8XY0(self):
        extracted_op = self.op_code & 0xf00f
       
        if extracted_op == 0x8000:
            print("Set VX = Vy")
            self.gpio[self.vx] = self.gpio[self.vy]
            pass
        else:
            try:
                self.funcmap[extracted_op]()
            except:
                print(f"Unknown instruction {hex(self.op_code)}")
                pass
            print("fin")

   
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
        print("in 8xy5")
        if self.gpio[self.vx] > self.gpio[self.vy]:
            self.gpio[0xf] = 1
        else:
            self.gpio[0xf] = 0
        self.gpio[self.vx] = self.gpio[self.vx] - self.gpio[self.vy]
        print("leaving 8xy5")
    
    #Harry's code
    # def _8XY6(self):
    #     print("Set Vx = Vx SHR 1.")
    #     if self.gpio[self.vx] & 0x1 == 1:
    #         self.gpio[0xf] = self.gpio[self.vx] & 0x1
    #     else:
    #         self.gpio[0xf] = 0 
    #     self.gpio[self.vx] >>= 1
    
    def _8XY6(self):
        print("Set Vx = Vx SHR 1.")
        if self.gpio[self.vx] & 0x01 == 1:
            self.gpio[0xf] = 1
        else:
            self.gpio[0xf] = 0 
        self.gpio[self.vx] = (self.gpio[self.vx] >> 1) & 0xff
    
    def _8XY7(self):
        print("Set Vx = Vy - Vx, set VF = NOT borrow.")
        if self.gpio[self.vy] > self.gpio[self.vx]:
            self.gpio[0xf] = 1
        else:
            self.gpio[0xf] = 0
        self.gpio[self.vx] = self.gpio[self.vy] - self.gpio[self.vx]
    

    #Harry's code
    def _8XYE(self):
        print("Set Vx = Vx SHL 1")
        if self.gpio[self.vx] & 0x1 == 1:
            self.gpio[0xf] = self.gpio[self.vx] & 0x1
        else:
            self.gpio[0xf] = 0 
        self.gpio[self.vx] <<= 1
    
    # def _8XYE(self):
    #     print("Set Vx = Vx SHL 1")
    #     if self.gpio[self.vy] & 0x80 == 0x80:
    #         self.gpio[0xf] = 1
    #     else:
    #         self.gpio[0xf] = 0 
    #     self.gpio[self.vx] = (self.gpio[self.vx] << 1) & 0xff
    
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
        self.gpio[self.vx] = random.randint(0,0xff) & (self.op_code & 0x00ff)

    def _DXYN(self):
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
    
    def _DXYN2(self):
        x = self.gpio[self.vx] & 0xff 
        y = self.gpio[self.vy] & 0xff
        height = self.op_code & 0x000f

        self.gpio[0xf] = 0

        for row in range(0,height):
            spriteByte = self.memory[self.index + row]
            for column in range(0,8):
                loc = x + column + ((y+row) * 64)
                if (y+row) >= 32 or (x + column - 1 >= 64):
                    continue
                mask = 1 << 7 - column
                curr_pixel = (spriteByte & mask) >> (7 - column)
                
                self.display_buffer[loc] ^= curr_pixel
                if self.display_buffer[loc] == 0:
                    self.gpio[0xf] = 1
            self.should_draw = True
    def _EZZZ(self):
        extracted_op = self.op_code & 0xf000
        print("In new function rn")
        try:
            self.funcmap[extracted_op]()
        except:
            print(f"Unknown instruction {hex(self.op_code)}")
            pass
        print("fin")

    def _EX9E(self):
        print("Skip next instruction if key with the value of Vx is pressed")
        if self.input_buffer[self.gpio[self.vx]] == 1:
            self.pc += 2
    
    def _EXA1(self):
        print("Skip next instruction if key with the value of Vx is not pressed.")
        if self.input_buffer[self.gpio[self.vx]] == 0:
            self.key_inputs 
            self.pc += 2
    
    def _FZZZ(self):
        extracted_op = self.op_code & 0xf0ff
        
       
        try:
            self.funcmap[extracted_op]()
        except:
            print(f"Unknown instruction {hex(self.op_code)}")
            pass
        print("fin")
    
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
        self.index = (5*(self.gpio[(self.op_code & 0x0F00) >> 8])) & 0xfff
        print("FX29 Complete")

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
        for addr in range(0,self.vx +1 ):
            self.gpio[addr] = self.memory[self.index + addr]





chip8emu = cpu(640,320)
chip8emu.main()

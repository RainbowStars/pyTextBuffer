# This is free and unencumbered software released into the public domain.
# 
# Anyone is free to copy, modify, publish, use, compile, sell, or
# distribute this software, either in source code form or as a compiled
# binary, for any purpose, commercial or non-commercial, and by any
# means.
# 
# In jurisdictions that recognize copyright laws, the author or authors
# of this software dedicate any and all copyright interest in the
# software to the public domain. We make this dedication for the benefit
# of the public at large and to the detriment of our heirs and
# successors. We intend this dedication to be an overt act of
# relinquishment in perpetuity of all present and future rights to this
# software under copyright law.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
# 
# For more information, please refer to <http://unlicense.org/>

from curses import *
from types import *

class TextBuffer:
    def __init__(self, window):
        self.window = window
        
        (self.win_max_y, self.win_max_x) = self.window.getmaxyx()
        
        self._buffer_ = u''
        self._scroll_page_horizontal = 0
        self._scroll_page_vertical = 0
        self._SCROLL_AMOUNT = 14
        
        # maps keystrokes/key constants to functions
        self.giant_dictionary = {
            # ^A
            1:          lambda c: self.jump_left(),
            # ^E
            5:          lambda c: self.jump_right(),
            # M / meta
            27:         {
                # b
                98:         lambda c: self.move_word_left(),
                # f
                102:        lambda c: self.move_word_right()
            },
            KEY_LEFT:   lambda c: self.move_left(),
            KEY_RIGHT:  lambda c: self.move_right(),
            KEY_UP:     lambda c: self.move_up(),
            KEY_DOWN:   lambda c: self.move_down(),
                        
            KEY_DC:     lambda c: self.delete_char_right()
        }
        
        # right now we only support windows one line high
        if self.window.getmaxyx()[0] > 1:
            raise Exception
    
    def edit(self,
             key_handler = (lambda k: k),
             termination_characters = ['\n']):
        self.key_handler = key_handler
        self.termination_characters = termination_characters
        
        return self.loop(self.giant_dictionary)
    
    def loop(self, dictionary):
        char = self.window.get_wch()
        
        # if dictionary is not giant_dictionary, then that means we are in a meta/dead key state
        if char not in self.termination_characters or dictionary is not self.giant_dictionary:
            if type(char) is str:
                key = ord(char)
            elif type(char) is int:
                key = char
            else:
                raise TypeError
            
            if key in dictionary:
                value = dictionary[key]
                
                if type(value) is FunctionType:
                    value(char)
                elif type(value) is dict:
                    return self.loop(value)
                else:
                    raise TypeError
            else:
                self.insert_char(char)
            
            return self.loop(self.giant_dictionary)
        else:
            new_buffer = self._buffer_
            self.delete_buffer()
            
            return new_buffer
    
    def scroll_left(self):
        self.window.clear()
        self.window.move(0, 0)
        
        self._scroll_page_horizontal += 1
        
        for c in self._buffer_[self._SCROLL_AMOUNT * self._scroll_page_horizontal:len(self._buffer_)]:
            self.window.addch(c)
    
    def scroll_right(self):
        if self._scroll_page_horizontal is not 0:
            self.window.clear()
            self.window.move(0, 0)
            
            self._scroll_page_horizontal -= 1
            
            for c in self._buffer_[self._SCROLL_AMOUNT * self._scroll_page_horizontal:min(len(self._buffer_), self.win_max_x)]:
                self.window.addch(c)
    
    def scroll_vertical(self):
        return
    
    def page_up(self):
        return
    
    def page_down(self):
        return
    
    def insert_char(self, char):
        (y, x) = self.window.getyx()
        (p, q) = self.window.getmaxyx()
        
        if x is q - 2:
            self.scroll_left()
        
        self.window.addch(char)
        self._buffer_ += str(char)
    
    def delete_char_left(self):
        return
    
    def delete_char_right(self):
        return
    
    def delete_word_left(self):
        return
    
    def delete_word_right(self):
        return
    
    def delete_line(self):
        return
    
    def delete_buffer(self):
        self._buffer_ = u''
        self._scroll_page_horizontal = 0
        self.window.clear()
        self.window.move(0, 0)
    
    def jump_left(self):
        self.window.move(0, 0)
        
        if not self._scroll_page_horizontal is 0:
            self.window.clear()
            self.window.move(0, 0)
            
            for c in self._buffer_[0:self.win_max_x]:
                self.window.addch(c)
            
            self.window.move(0, 0)
            
    def jump_right(self):
        return
    
    def jump_up(self):
        return
    
    def jump_down(self):
        return
    
    def move_left(self):
        (y, x) = self.window.getyx()
        
        if self._scroll_page_horizontal is not 0 and x is 1:
            self.scroll_right()
        
        self.window.move(y, max(0, x - 1))
    
    def move_right(self):
        (y, x) = self.window.getyx()
        
        if (not self.buffer_position() is len(self._buffer_)):
            if x is self.win_max_x - 1:
                self.scroll_left()
            
            self.window.move(y, x + 1)
    
    def move_up(self):
        return
    
    def move_down(self):
        return
    
    def move_word_left(self):
        return
    
    def move_word_right(self):
        return
    
    # returns the position of the cursor relative to _buffer_
    def buffer_position(self):
        (y, x) = self.window.getyx()
        return (self._scroll_page_horizontal * self._SCROLL_AMOUNT) + x
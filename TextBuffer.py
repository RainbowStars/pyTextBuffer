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

# replacement for Python's curses.textpad.Textbox object
class TextBuffer:
    global _SCROLL_AMOUNT
    _SCROLL_AMOUNT = 14
    
    def __init__(self, window):
        self.window = window
        
        self._buffer_ = u''
        self._scroll_h_ = 0
        self._scroll_page_horizontal = 0
        self._scroll_page_vertical = 0
        self._SCROLL_AMOUNT = 14
        
        # maps keystrokes/key constants to functions
        self.giant_dictionary = {
            KEY_LEFT:   lambda c: self.move_left(),
            KEY_RIGHT:  lambda c: self.move_right(),
            KEY_UP:     lambda c: self.move_up(),
            KEY_DOWN:   lambda c: self.move_down()
        }
        
        if self.window.getmaxyx()[0] > 1:
            raise Exception
    
    def edit(self,
             key_handler = (lambda k: k),
             termination_characters = ['\n']):
        self.key_handler = key_handler
        self.termination_characters = termination_characters
        return self.loop()
    
    def loop(self):
        ch = self.window.get_wch()
        
        if not ch in self.termination_characters:
            if type(ch) is int:
                if ch in self.giant_dictionary:
                    self.giant_dictionary[ch](ch)
            elif type(ch) is str:
                self.insert_char(ch)
            else:
                raise TypeError
            
            return self.loop()
        else:
            new_buffer = self._buffer_
            self.delete_buffer()
            return new_buffer
    
    def scroll_left(self):
        self.window.clear()
        self.window.move(0, 0)
        
        self._scroll_h_ += 1
        
        for c in self._buffer_[self._SCROLL_AMOUNT * self._scroll_h_:len(self._buffer_)]:
            self.window.addch(c)
    
    def scroll_right(self):
        if self._scroll_h_ is not 0:
            self.window.clear()
            self.window.move(0, 0)
            
            self._scroll_h_ -= 1
            
            for c in self._buffer_[self._SCROLL_AMOUNT * self._scroll_h_:len(self._buffer_)]:
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
        self._scroll_h_ = 0
        self.window.clear()
        self.window.move(0, 0)
    
    def jump_left(self):
        (p, q) = self.window.getmaxyx()
        
        if self._scroll_h_ == 0:
            self.window.move(0,0)
        else:
            self.window.clear()
            self.window.move(0,0)
            
            for c in self._buffer_[0:q]:
                self.window.addch(c)
            
            self.window.move(0,0)
    
    def jump_right(self):
        return
    
    def jump_up(self):
        return
    
    def jump_down(self):
        return
    
    def move_left(self):
        (y, x) = self.window.getyx()
        
        if self._scroll_h_ is not 0 and x is 1:
            self.scroll_right()
        if not (self._scroll_h_ is 0 and x is 0):
            self.window.move(y, max(0, x - 1))
    
    def move_right(self):
        
        (y, x) = self.window.getyx()
        
        if self._scroll_h_ is 0:
            self.window.move(y, max(0, x - 1))
        else:
            return
    
    def move_up(self):
        return
    
    def move_down(self):
        return
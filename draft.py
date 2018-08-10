a = [1, 2, 3]
print("%d  %d" % (False, True))


def callback_arrow(self, n):
    def make_move(sth):
        if n < 8:
            if self.now_player == 1:
                if n == 0:
                    self.Cur_pos = do_move_nochange(self.Cur_pos, tuple((0, 0, self.Cur_pos[0], 0)))
                elif n == 1:
                    self.Cur_pos = do_move_nochange(self.Cur_pos, tuple((0, 0, 0, self.Cur_pos[0])))
                elif n == 2:
                    self.Cur_pos = do_move_nochange(self.Cur_pos, tuple((0, 0, 0, self.Cur_pos[1])))
                elif n == 3:
                    self.Cur_pos = do_move_nochange(self.Cur_pos, tuple((0, 0, self.Cur_pos[1], 0)))
            else:
                elif n == 4:
                self.Cur_pos = do_move_nochange(self.Cur_pos, tuple((self.Cur_pos[2], 0, 0, 0)))
            elif n == 5:
            self.Cur_pos = do_move_nochange(self.Cur_pos, tuple((0, self.Cur_pos[2], 0, 0)))
        elif n == 6:
            self.Cur_pos = do_move_nochange(self.Cur_pos, tuple((0, self.Cur_pos[3], 0, 0)))
        else:
            self.Cur_pos = do_move_nochange(self.Cur_pos, tuple((self.Cur_pos[3], 0, 0, 0)))


self.draw_fingers()
if not primitive(self.Cur_pos) == UNKNOWN:
    self.game_end()
return make_move


"""
import pickle
from tkinter import *
from PIL import Image, ImageTk

# string of the status
class Value:
    def __init__(self):
        self.WIN = "WIN"
        self.LOSE = "LOSE"
        self.TIE = "TIE"
        self.DRAW = "DRAW"
        self.UNKNOWN = "UNKNOWN"


class GameOption:
    def __init__(self):
        self.max_fingers = 3
        self.rules = "China"  # or "US"
        self.enable_mod = 1  # 1:get to 0(mod max_fingers) OR 0:first above max_fingers
        self.enable_self_share = 0  # switch number oneself
        self.self_share_mode = 0  # 0:only if different   1:(1,2)to(2,1)is OK
        self.enable_wake_dead_hand = 0

    def into_string(self):
        return "%d%s%d%d%d%d" % (self.max_fingers, self.rules, self.enable_mod, self.enable_self_share,
                                 self.self_share_mode, self.enable_wake_dead_hand)

class Game:
    def __init__(self):  # default case
        self.option = GameOption()
        self.Init_Pos = [1, 1, 1, 1]
        self.Database = {}
        self.value = Value()
        self.hands = []

        self.Cur_pos = [1, 1, 1, 1]

        self.database_path = self.option.into_string() + ".pkl"

        self.image_list = []
        for i in range(10):
            self.image_list.append(ImageTk.PhotoImage(Image.open('number\\%d.png' % (i + 1))))

        self.move_record = []
        self.move_pos = -1

    def open_database(self):
        try:
            f = open(self.database_path, 'rb')
            self.Database = pickle.load(f)
            f.close()
            return True
        except IOError:
            return False

    def exist_database(self):
        return self.open_database()

    def reset(self, change):
        if change == 1 and self.option.max_fingers < 9:
            self.option.max_fingers += 1
        elif change == 2 and self.option.max_fingers > 2:
            self.option.max_fingers -= 1
        elif change == 3:
            if self.option.rules == "China":
                self.option.rules = "US"
            else:
                self.option.rules = "China"
        elif change == 4:
            self.option.enable_self_share = not self.option.enable_self_share
        elif change == 5:
            self.option.self_share_mode = 3 - self.option.self_share_mode
        elif change == 6:
            self.option.enable_wake_dead_hand = not self.option.enable_wake_dead_hand

        self.database_path = self.option.into_string()

    def draw_interface(self, r):
        p1l = Label(r, image=self.image_list[0])
        p1r = Label(r, image=self.image_list[0])
        p2l = Label(r, image=self.image_list[0])
        p2r = Label(r, image=self.image_list[0])
        self.hands = [p1l, p1r, p2l, p2r]
        p1l.place(x=100, y=100)
        p1r.place(x=400, y=100)
        p2l.place(x=100, y=400)
        p2r.place(x=400, y=400)

    def callback_start(self):
        (self.hands[0]).config(image=self.image_list[0])
        (self.hands[1]).config(image=self.image_list[0])
        (self.hands[2]).config(image=self.image_list[0])
        (self.hands[3]).config(image=self.image_list[0])

    def callback_redo(self):
        return

    def callback_undo(self):
        return

    def callback_show(self):
        return

    def callback_player1(self):
        return

    def callback_player2(self):
        return

    def dict_hash(self, pos):
        return 1000 * pos[0] + 100 * pos[1] + 10 * pos[2] + pos[0]

    def do_move(self, position, move):
        new = position
        new[move[0]] += position[move[1]]
        if new[move[0]] == self.option.max_fingers:
            new[move[0]] = 0
        return new

    def gen_moves(self, position):
        result = []
        if position[0] > 0:
            if position[2] > 0 and position[0] + position[2] <= self.option.max_fingers:
                result.append(tuple((0, 2)))
            if position[3] > 0 and position[0] + position[3] <= self.option.max_fingers:
                result.append(tuple((0, 3)))
        if position[1] > 0:
            if position[2] > 0 and position[1] + position[2] <= self.option.max_fingers:
                result.append(tuple((1, 2)))
            if position[3] > 0 and position[1] + position[3] <= self.option.max_fingers:
                result.append(tuple((1, 3)))
        return result

    def is_primitive(self, position):
        if self.option.rules == "China":
            if position[2] == 0 and position[3] == 0:
                return True
            elif position[0] == 0 and position[1] == 0:
                return True
            else:
                return False
        else:
            if position[0] == 0 and position[1] == 0:
                return True
            else:
                return False

    def primitive(self, position):
        if self.option.rules == "China":
            if position[2] == 0 and position[3] == 0:
                return self.value.LOSE
            else:
                return self.value.WIN
        else:
            if position[0] == 0 and position[1] == 0:
                return True
            else:
                return False

    def do_back_move(position, move):
        return

    def gen_back_moves(self, position):
        result = []
        return result

    def get_children(self, position):
        return [self.do_move(position, move) for move in self.gen_moves(position)]

    def get_parent(self, position):
        return [self.do_back_move(position, move) for move in self.gen_back_moves(position)]

    @staticmethod
    def print_intro():
        print("This Game is a counting game.\nAna and Bob take turns to add a number from a given list "
              "to the initial number.\nWho reaches the given number which represents ENDING first, who wins.")

"""
import pickle
from tkinter import *
from PIL import Image, ImageTk
import time
# API Application Programming Interface
# position is a tuple, its format is (player hand1, player hand2, opponent hand1, opponent hand2), assume hand1 < hand2

import solver

WIN = "win"
LOSE = "lose"
TIE = "tie"
UNKNOWN = "unknown"
DRAW = "draw"

CHINESE_RULE = True  # opposite: US_RULE
SELF_SHARE = False
PASS_RULE = False
FINGER_NUMBER = 5


def primitive(position):
    if CHINESE_RULE:
        if position[2] == 0 and position[3] == 0:
            return LOSE
    else:
        if position[0] == 0 and position[1] == 0:
            return WIN
    return UNKNOWN


def gen_moves(position):
    possible_move = [(position[2], 0, 0, 0), (0, position[2], 0, 0), (position[3], 0, 0, 0), (0, position[3], 0, 0),
    (0, 0, position[0], 0), (0, 0, 0, position[0]), (0, 0, position[1], 0), (0, 0, 0, position[1])]
    moves = []
    if CHINESE_RULE:
        if position[2] != 0 and position[0] != 0:
            moves.append(possible_move[0])
        if position[2] != 0:
            moves.append(possible_move[1])
        if position[0] != 0:
            moves.append(possible_move[2])
        moves.append(possible_move[3])
    else:
        if position[2] != 0 and position[0] != 0:
            moves.append(possible_move[4])
        if position[2] != 0:
            moves.append(possible_move[6])
        if position[0] != 0:
            moves.append(possible_move[5])
        moves.append(possible_move[7])
    if PASS_RULE:
        moves.append((0, 0, 0, 0))
    output = []
    for x in moves:
        if x not in output:
            output.append(x)
    return output


def do_move(position, move):
    new_position = [(position[i] + move[i]) % FINGER_NUMBER for i in range(4)]
    right = new_position[0:2]
    left = new_position[2:4]
    right.sort()
    left.sort()
    left.extend(right)
    return tuple(left)

def ddo_move(position, move):
    new_position = [(position[i] + move[i]) % FINGER_NUMBER for i in range(4)]
    return new_position

do_backmove = do_move
VALUES = {}


def gen_backmoves(position):
    possible_move = [(-position[2], 0, 0, 0), (0, -position[2], 0, 0), (-position[3], 0, 0, 0), (0, -position[3], 0, 0),
    (0, 0, -position[0], 0), (0, 0, 0, -position[0]), (0, 0, -position[1], 0), (0, 0, 0, -position[1])]
    moves = []
    if CHINESE_RULE:
        if position[0] != 0:
            moves.append(possible_move[4])
            moves.append(possible_move[5])
        moves.append(possible_move[6])
        moves.append(possible_move[7])
    else:
        if position[2] != 0:
            moves.append(possible_move[0])
            moves.append(possible_move[1])
        moves.append(possible_move[2])
        moves.append(possible_move[3])
    if PASS_RULE:
        moves.append((0, 0, 0, 0))
    output = []
    for x in moves:
        if x not in output:
            output.append(x)
    return output


def children(position):
    t = [do_move(position, move) for move in gen_moves(position)]
    output = []
    for x in t:
        if x not in output:
            output.append(x)
    return output


def parent(position):
    t = [do_backmove(position, move) for move in gen_backmoves(position)]
    output = []
    for x in t:
        if x not in output and x.count(0) <= position.count(0):
            output.append(x)
    return output


triangle_loc = [[160, 200, 240, 200, 200, 400], [160, 200, 240, 200, 390, 400],
                [350, 200, 430, 200, 390, 400], [350, 200, 430, 200, 200, 400],  # player 1

                [240, 400, 160, 400, 200, 200], [240, 400, 160, 400, 390, 200],
                [350, 400, 430, 400, 390, 200], [350, 400, 430, 400, 200, 200],  # player 2

                [270, 90, 290, 80, 290, 100], [320, 90, 300, 80, 300, 100],
                [270, 510, 290, 500, 290, 520], [320, 510, 300, 500, 300, 520]]  # self-share


class GameControl:
    def __init__(self, root, canvas):
        self.root = root
        self.canvas = canvas
        self.canvas.pack()

        self.hands = []
        self.Cur_pos = [1, 1, 1, 1]

        self.now_player = 1
        self.player_type = [0, 1]  # 0:human  1:computer

        self.IsPlaying = False

        self.image_list = []
        for i in range(10):
            self.image_list.append(ImageTk.PhotoImage(Image.open('number\\%d.png' % i)))

        self.move_record = []
        self.move_pos = -1

        self.self_share_rec = 0

        self.show_value = False

        self.button = []
        self.message = []
        self.triangle = []

        self.Database = {}
        if not self.load_database():
            self.build_database()

    @staticmethod
    def option_into_str():
        return "%d%d%d%d" % (FINGER_NUMBER, CHINESE_RULE, SELF_SHARE, PASS_RULE)

    def load_database(self):
        file_path = self.option_into_str() + '.pkl'
        try:
            f = open(file_path, 'rb')
            self.Database = pickle.load(f)
            f.close()
            return True
        except IOError:
            return False

    def build_database(self):
        file_path = self.option_into_str() + '.pkl'
        solver.solve(tuple(self.Cur_pos))
        f = open(file_path, 'wb')
        pickle.dump(solver.Tree, f)
        self.Database = solver.Tree
        f.close()

    def draw_interface(self):
        p1l = Label(self.root, image=self.image_list[1])
        p1r = Label(self.root, image=self.image_list[1])
        p2l = Label(self.root, image=self.image_list[1])
        p2r = Label(self.root, image=self.image_list[1])
        self.hands = [p1l, p1r, p2l, p2r]
        p1l.place(x=140, y=50)
        p1r.place(x=340, y=50)
        p2l.place(x=140, y=400)
        p2r.place(x=340, y=400)

        self.button.append(Button(self.root, text='RULES:CHINA', width=20, height=2,
                                  command=self.callback_rules))
        self.button[7].place(x=600, y=10)
        #self.button.append(Button(self.root, text='SELF_SHARE:OFF', width=20, height=2,
         #                         command=self.callback_self_share))
        #self.button[8].place(x=600, y=70)
        #self.button.append(Button(self.root, text='PASS:OFF', width=20, height=2,
        #                          command=self.callback_pass))
        #self.button[8].place(x=600, y=130)
        self.button.append(Button(self.root, text='GOAL:REACH %d' % FINGER_NUMBER, width=20, height=2,
                                  command=self.callback_fingers))
        self.button[8].place(x=600, y=190)

        #self.button.append(Button(self.root, text='SHARE FINISH', width=12, height=1,
        #                       command=self.callback_fingers))
        #if SELF_SHARE:
         #   self.button[11].place(x=40, y=40)

        Label(self.root, text="Player 1").place(x=80, y=80)
        Label(self.root, text="Player 2").place(x=80, y=450)

    def draw_fingers(self):
        (self.hands[0]).config(image=self.image_list[self.Cur_pos[0]])
        (self.hands[1]).config(image=self.image_list[self.Cur_pos[1]])
        (self.hands[2]).config(image=self.image_list[self.Cur_pos[2]])
        (self.hands[3]).config(image=self.image_list[self.Cur_pos[3]])

    def make_choice(self):
        mylist = children(self.Cur_pos)
        if self.Database[self.Cur_pos][1] == WIN:
            for item in mylist:
                if self.Database[item][1] == LOSE:
                    self.Cur_pos = item
                    self.Cur_pos = do_move(self.Cur_pos, tuple((0, 0, 0, 0)))
        else:
            self.Cur_pos = mylist[0]
            self.Cur_pos = do_move(self.Cur_pos, tuple((0, 0, 0, 0)))

    def animation(self):
        #self.draw_fingers()
        #time.sleep(0.5)
        #self.make_choice()
        self.set_arrow()

    def callback_start(self):
        self.Cur_pos = [1, 1, 1, 1]
        self.move_record.clear()
        self.move_pos = 0
        self.now_player = 1
        self.draw_fingers()
        self.message[0].config(text="A new Game!")
        self.IsPlaying = True
        if not self.load_database():
            self.build_database()
        if self.player_type[self.now_player - 1] == 0:
            self.set_arrow()
        else:
            self.animation()

    def callback_end(self):
        self.IsPlaying = False
        self.canvas.delete("all")

    def callback_undo(self):
        if self.IsPlaying:
            if self.move_pos > 0:
                self.move_pos -= 1
                self.Cur_pos = self.move_record[self.move_pos]
                self.draw_fingers()
                self.now_player = 3 - self.now_player
                self.set_arrow()

    def callback_redo(self):
        if self.IsPlaying:
            self.move_pos += 1
            try:
                self.Cur_pos = self.move_record[self.move_pos]
                self.draw_fingers()
                self.now_player = 3 - self.now_player
                self.set_arrow()
            except IndexError:
                self.move_pos -= 1

    def callback_show_value(self):
        if self.show_value:
            self.button[3].config(text="SHOW MOVE'S VALUE")
            self.show_value = False
        else:
            self.button[3].config(text="NOSHOW")
            self.show_value = True
        if not self.load_database():
            self.build_database()

    def callback_player1(self):
        if not self.IsPlaying:
            if self.player_type[0] == 1:
                self.message[0].config(text="Now Player1 is Human!")
                self.player_type[0] = 0
                self.button[4].config(text='PLAYER1:\nHuman')
            else:
                self.message[0].config(text="Now Player1 is Computer!")
                self.player_type[0] = 1
                self.button[4].config(text='PLAYER1:\nComputer')
        else:
            self.message[0].config(text="You must press END to end game played now!!!")

    def callback_player2(self):
        if not self.IsPlaying:
            if self.player_type[1] == 1:
                self.message[0].config(text="Now Player2 is Human!")
                self.player_type[1] = 0
                self.button[5].config(text='PLAYER2:\nHuman')
            else:
                self.message[0].config(text="Now Player2 is Computer!")
                self.player_type[1] = 1
                self.button[5].config(text='PLAYER2:\nComputer')
        else:
            self.message[0].config(text="You must press END to end game played now!!!")

    def callback_rules(self):
        if not self.IsPlaying:
            global CHINESE_RULE
            if CHINESE_RULE:
                CHINESE_RULE = False
                self.button[7].config(text="RULES:US")
            else:
                CHINESE_RULE = True
                self.button[7].config(text="RULES:CHINA")
            self.message[0].config(text="CHINA:who reach the goal, who wins. US:just the opposite!")
        else:
            self.message[0].config(text="You must press END to end game played now!!!")
        if not self.load_database():
            self.build_database()

    def callback_self_share(self):
        if not self.IsPlaying:
            global SELF_SHARE
            if SELF_SHARE:
                SELF_SHARE = False
                self.button[8].config(text='SELF_SHARE:OFF')
                self.button[11].place_forget()
            else:
                SELF_SHARE = True
                self.button[8].config(text='SELF_SHARE:ON')
                self.button[11].place(x=50, y=50)
            self.message[0].config(text="if SELF_SHARE is ON, it means that you can transfer number on your hands.")
        else:
            self.message[0].config(text="You must press END to end game played now!!!")
        if not self.load_database():
            self.build_database()

    def callback_pass(self):
        if not self.IsPlaying:
            global PASS_RULE
            if PASS_RULE:
                PASS_RULE = False
                self.button[9].config(text='PASS:OFF')
            else:
                PASS_RULE = True
                self.button[9].config(text='PASS:ON')
            self.message[0].config(text="if PASS is ON, it means that you can do nothing when it turns to you.")
        else:
            self.message[0].config(text="You must press END to end game played now!!!")
        if not self.load_database():
            self.build_database()

    def callback_fingers(self):
        if not self.IsPlaying:
            global FINGER_NUMBER
            if FINGER_NUMBER < 10:
                FINGER_NUMBER += 1
            else:
                FINGER_NUMBER = 2
            self.message[0].config(text="GOAL means that whose both hands reach that number, the game is over")
            self.button[8].config(text='GOAL:REACH %d' % FINGER_NUMBER)
        else:
            self.message[0].config(text="You must press END to end game played now!!!")
        if not self.load_database():
            self.build_database()

    def game_end(self):
        sss = primitive(self.Cur_pos)
        if sss == UNKNOWN:
            sss = WIN
        self.message[0].config(text="Player %d %s. Game Over." % (self.now_player, sss))
        self.callback_end()

    def get_color(self, pos, m):
        if not self.show_value:
            return 'white'
        new = tuple(ddo_move(pos, m))
        sss = primitive(new)
        if not sss == UNKNOWN:
            if sss == WIN:
                return 'green'
            if sss == LOSE:
                return 'red'
        try:
            if self.Database[new][1] == WIN:
                return 'green'
            elif self.Database[new][1] == LOSE:
                return 'red'
            else:
                return 'yellow'
        except KeyError:
            return 'black'

    def set_arrow(self):
        if self.IsPlaying:
            self.canvas.delete("all")
            self.triangle.clear()
            ddd = False
            if self.now_player == 1:
                if self.Cur_pos[0] > 0:
                    if self.Cur_pos[2] > 0:
                        s = self.get_color(self.Cur_pos, tuple((0, 0, self.Cur_pos[0], 0)))
                        x = self.canvas.create_polygon(triangle_loc[0], outline='white',
                                                       fill=s, activefill='violet')
                        self.triangle.append(x)
                        self.canvas.tag_bind(x, sequence="<Button-1>", func=self.callback_arrow(0))
                        ddd = True
                    if self.Cur_pos[3] > 0:
                        s = self.get_color(self.Cur_pos, tuple((0, 0, 0, self.Cur_pos[0])))
                        x = self.canvas.create_polygon(triangle_loc[1], outline='white',
                                                       fill=s, activefill='violet')
                        self.triangle.append(x)
                        self.canvas.tag_bind(x, sequence="<Button-1>", func=self.callback_arrow(1))
                        ddd = True
                if self.Cur_pos[1] > 0:
                    if self.Cur_pos[2] > 0:
                        s = self.get_color(self.Cur_pos, tuple((0, 0, self.Cur_pos[1], 0)))
                        x = self.canvas.create_polygon(triangle_loc[3], outline='white',
                                                       fill=s, activefill='violet')
                        self.triangle.append(x)
                        self.canvas.tag_bind(x, sequence="<Button-1>", func=self.callback_arrow(3))
                        ddd = True
                    if self.Cur_pos[3] > 0:
                        s = self.get_color(self.Cur_pos, tuple((0, 0, 0, self.Cur_pos[1])))
                        x = self.canvas.create_polygon(triangle_loc[2], outline='white',
                                                       fill=s, activefill='violet')
                        self.triangle.append(x)
                        self.canvas.tag_bind(x, sequence="<Button-1>", func=self.callback_arrow(2))
                        ddd = True
            else:
                if self.Cur_pos[2] > 0:
                    if self.Cur_pos[0] > 0:
                        s = self.get_color(self.Cur_pos, tuple((self.Cur_pos[2], 0, 0, 0)))
                        x = self.canvas.create_polygon(triangle_loc[4], outline='white',
                                                       fill=s, activefill='violet')
                        self.triangle.append(x)
                        self.canvas.tag_bind(x, sequence="<Button-1>", func=self.callback_arrow(4))
                        ddd = True
                    if self.Cur_pos[1] > 0:
                        s = self.get_color(self.Cur_pos, tuple((0, self.Cur_pos[2], 0, 0)))
                        x = self.canvas.create_polygon(triangle_loc[5], outline='white',
                                                       fill=s, activefill='violet')
                        self.triangle.append(x)
                        self.canvas.tag_bind(x, sequence="<Button-1>", func=self.callback_arrow(5))
                        ddd = True
                if self.Cur_pos[3] > 0:
                    if self.Cur_pos[0] > 0:
                        s = self.get_color(self.Cur_pos, tuple((self.Cur_pos[3], 0, 0, 0)))
                        x = self.canvas.create_polygon(triangle_loc[7], outline='white',
                                                       fill=s, activefill='violet')
                        self.triangle.append(x)
                        self.canvas.tag_bind(x, sequence="<Button-1>", func=self.callback_arrow(7))
                        ddd = True
                    if self.Cur_pos[1] > 0:
                        s = self.get_color(self.Cur_pos, tuple((0, self.Cur_pos[3], 0, 0)))
                        x = self.canvas.create_polygon(triangle_loc[6], outline='white',
                                                       fill=s, activefill='violet')
                        self.triangle.append(x)
                        self.canvas.tag_bind(x, sequence="<Button-1>", func=self.callback_arrow(6))
                        ddd = True
            self.draw_fingers()
            if not ddd:
                self.game_end()

    def callback_arrow(self, n):
        def make_move(sth):
            if self.IsPlaying:
                if self.now_player == 1:
                    if n < 4:
                        if n == 0 and self.Cur_pos[0] > 0:
                            self.move_record.append(self.Cur_pos)
                            self.move_pos += 1
                            self.Cur_pos = ddo_move(self.Cur_pos, tuple((0, 0, self.Cur_pos[0], 0)))
                            self.now_player = 2
                            if not primitive(self.Cur_pos) == UNKNOWN:
                                self.game_end()
                        elif n == 1 and self.Cur_pos[0] > 0:
                            self.move_record.append(self.Cur_pos)
                            self.move_pos += 1
                            self.Cur_pos = ddo_move(self.Cur_pos, tuple((0, 0, 0, self.Cur_pos[0])))
                            #self.Cur_pos = ddo_move(self.Cur_pos, tuple((0, 0, 0, self.Cur_pos[0])))
                            self.now_player = 2
                            if not primitive(self.Cur_pos) == UNKNOWN:
                                self.game_end()
                        elif n == 2 and self.Cur_pos[1] > 0:
                            self.move_record.append(self.Cur_pos)
                            self.move_pos += 1
                            self.Cur_pos = ddo_move(self.Cur_pos, tuple((0, 0, 0, self.Cur_pos[1])))
                            #self.Cur_pos = ddo_move(self.Cur_pos, tuple((0, 0, 0, self.Cur_pos[1])))
                            self.now_player = 2
                            if not primitive(self.Cur_pos) == UNKNOWN:
                                self.game_end()
                        elif n == 3 and self.Cur_pos[1] > 0:
                            self.move_record.append(self.Cur_pos)
                            self.move_pos += 1
                            self.Cur_pos = ddo_move(self.Cur_pos, tuple((0, 0, self.Cur_pos[1], 0)))
                            #self.Cur_pos = ddo_move(self.Cur_pos, tuple((0, 0, self.Cur_pos[1], 0)))
                            self.now_player = 2
                            if not primitive(self.Cur_pos) == UNKNOWN:
                                self.game_end()
                    else:
                        if n == 8:
                            self.Cur_pos = do_move(self.Cur_pos, tuple((1, -1, 0, 0)))
                        elif n == 9:
                            self.Cur_pos = do_move(self.Cur_pos, tuple((-1, 1, 0, 0)))
                else:
                    if 3 < n < 8:
                        if n == 4 and self.Cur_pos[2] > 0:
                            self.move_record.append(self.Cur_pos)
                            self.move_pos += 1
                            self.Cur_pos = ddo_move(self.Cur_pos, tuple((self.Cur_pos[2], 0, 0, 0)))
                            #self.Cur_pos = ddo_move(self.Cur_pos, tuple((self.Cur_pos[0], 0, 0, 0)))
                            self.now_player = 1
                            if not primitive(self.Cur_pos) == UNKNOWN:
                                self.game_end()
                        elif n == 5 and self.Cur_pos[2] > 0:
                            self.move_record.append(self.Cur_pos)
                            self.move_pos += 1
                            self.Cur_pos = ddo_move(self.Cur_pos, tuple((0, self.Cur_pos[2], 0, 0)))
                            #self.Cur_pos = ddo_move(self.Cur_pos, tuple((0, self.Cur_pos[2], 0, 0)))
                            self.now_player = 1
                            if not primitive(self.Cur_pos) == UNKNOWN:
                                self.game_end()
                        elif n == 6 and self.Cur_pos[3] > 0:
                            self.move_record.append(self.Cur_pos)
                            self.move_pos += 1
                            self.Cur_pos = ddo_move(self.Cur_pos, tuple((0, self.Cur_pos[3], 0, 0)))
                            #self.Cur_pos = ddo_move(self.Cur_pos, tuple((0, self.Cur_pos[3], 0, 0)))
                            self.now_player = 1
                            if not primitive(self.Cur_pos) == UNKNOWN:
                                self.game_end()
                        elif n == 7 and self.Cur_pos[3] > 0:
                            self.move_record.append(self.Cur_pos)
                            self.move_pos += 1
                            self.Cur_pos = ddo_move(self.Cur_pos, tuple((self.Cur_pos[3], 0, 0, 0)))
                            #self.Cur_pos = ddo_move(self.Cur_pos, tuple((self.Cur_pos[3], 0, 0, 0)))
                            self.now_player = 1
                            if not primitive(self.Cur_pos) == UNKNOWN:
                                self.game_end()
                    else:
                        if n == 8:
                            self.Cur_pos = do_move(self.Cur_pos, tuple((1, -1, 0, 0)))
                        elif n == 9:
                            self.Cur_pos = do_move(self.Cur_pos, tuple((-1, 1, 0, 0)))
            self.draw_fingers()
            if self.player_type[self.now_player - 1] == 0:
                self.set_arrow()
            else:
                self.animation()
        return make_move

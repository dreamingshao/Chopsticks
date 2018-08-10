from tkinter import *

import chopsticks as Game
import solver


def common_interface(ctrl):
    r = ctrl.root
    r.title("HAVE FUN!")
    r.geometry("1000x600")

    ctrl.button.clear()
    ctrl.button.append(Button(r, text='GAME START', width=20, height=2, command=ctrl.callback_start))
    ctrl.button[0].place(x=850, y=10)
    ctrl.button.append(Button(r, text='UNDO', width=8, height=2, command=ctrl.callback_undo))
    ctrl.button[1].place(x=850, y=60)
    ctrl.button.append(Button(r, text='REDO', width=8, height=2, command=ctrl.callback_redo))
    ctrl.button[2].place(x=925, y=60)

    ctrl.button.append(Button(r, text="SHOW MOVE'S VALUE", width=20, height=2, command=ctrl.callback_show_value))
    ctrl.button[3].place(x=850, y=130)

    ctrl.button.append(Button(r, text='PLAYER1:\nHuman', width=8, height=2, command=ctrl.callback_player1))
    ctrl.button[4].place(x=850, y=200)
    ctrl.button.append(Button(r, text='PLAYER2:\nComputer', width=8, height=2, command=ctrl.callback_player2))
    ctrl.button[5].place(x=925, y=200)

    ctrl.button.append(Button(r, text='End', width=20, height=2, command=ctrl.callback_end))
    ctrl.button[6].place(x=850, y=270)

    ctrl.message.clear()
    ctrl.message.append(Message(r, text="Welcome to play games!", width=130))
    ctrl.message[0].place(x=850, y=340)


if __name__ == "__main__":
    root = Tk()

    control = Game.GameControl(root, Canvas(root, width=1000, height=600))

    common_interface(control)
    control.draw_interface()

    root.mainloop()

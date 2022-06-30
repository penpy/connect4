import numpy as np
from copy import deepcopy
from tkinter import Button, Frame, Label, Menu, Tk
from tkinter import messagebox
from PIL import Image, ImageTk


class fGame:
    
    def __init__(self, length=8, height=8):
        self.grid = np.zeros((length, height), dtype=np.int8)
        self.height = height
        self.length = length
        
        x = np.zeros((length-3,length), dtype=bool)
        for i in range(length-3):
            z = np.zeros(length)
            z[i:i+4] = 1
            x[i] = z
        self.test_ver = x.reshape(1,length-3,length)

        y = np.zeros((height-3,height), dtype=bool)
        for i in range(height-3):
            z = np.zeros(height)
            z[i:i+4] = 1
            y[i] = z
        self.test_hor = y.reshape(height-3, height,1)
        
    def turn(self, player, row):
        for col in range(self.height):
            if self.grid[row, col] == 0:
                self.grid[row, col] = player
                return self.grid
        raise Exception("column full")
        
    def win(self):
        
        grid_ones = (self.grid == 1).reshape(1, self.length, self.height)
        grid_twos = (self.grid == 2).reshape(1, self.length, self.height)
        
        if np.max(np.dot(grid_ones, self.test_hor)) >= 4:
            return 1
        if np.max(np.dot(grid_twos, self.test_hor)) >= 4:
            return 2
        if np.max(np.dot(self.test_ver, grid_ones)) >= 4:
            return 1
        if np.max(np.dot(self.test_ver, grid_twos)) >= 4:
            return 2

        nb_diag = self.height + self.length - 7
        for dgd in range(nb_diag):
            
            counter_p1 = 0
            counter_p2 = 0
            nb_cells_dg = min(self.length, self.height, 4 + dgd, nb_diag - dgd + 3)
            col_0 = max(0, self.height - 4 - dgd)
            row_0 = max(0, dgd - self.height + 4)
            for i in range(nb_cells_dg):
                if self.grid[row_0 + i, col_0 + i] == 1:
                    counter_p1 += 1
                    counter_p2 = 0
                    if counter_p1 == 4:
                        return 1
                elif self.grid[row_0 + i, col_0 + i] == 2:
                    counter_p1 = 0
                    counter_p2 += 1
                    if counter_p2 == 4:
                        return 2
                else:
                    counter_p1 = 0
                    counter_p2 = 0
        
        for dga in range(nb_diag):
            counter_p1 = 0
            counter_p2 = 0
            nb_cells_dg = min(self.length, self.height, 4 + dga, nb_diag - dga + 3)
            row_0 = min(self.length - 1, 3 + dga)
            col_0 = max(0, dga - self.length + 4)
            
            for i in range(nb_cells_dg):
                if self.grid[row_0 - i, col_0 + i] == 1:
                    counter_p1 += 1
                    counter_p2 = 0
                    if counter_p1 == 4:
                        return 1
                elif self.grid[row_0 - i, col_0 + i] == 2:
                    counter_p1 = 0
                    counter_p2 += 1
                    if counter_p2 == 4:
                        return 2
                else:
                    counter_p1 = 0
                    counter_p2 = 0
                
        return 0  # no winner


class Game:

    def __init__(self, length=8, height=8):
        self.grid = np.zeros((length, height), dtype=np.int8)
        self.height = height
        self.length = length
        self.winner = self.win()
        self.history = []

    def clear_grid(self):
        self.grid = np.zeros((self.length, self.height), dtype=np.int8)
        self.history.clear()

    def turn(self, player, row):
        assert player == 1 or player == 2
        if row==None or player==None:
            return self.grid
        assert row >=0 and row < self.length and (type(row)==int or type(row)==np.int64)
        for col in range(self.height):
            if self.grid[row, col] == 0:
                self.grid[row, col] = player
                self.history.append((row, col))
                return self.grid
        raise Exception("column full")

    def remove(self, row):
        assert row >=0 and row < self.length and (type(row)==int or type(row)==np.int64) and self.grid[row, col]!=0
        top_not_empty = -1
        for col in range(self.height):
            if self.grid[row, col] != 0:
                top_not_empty += 1
        self.grid[row, top_not_empty] = 0
        self.history.remove((row, top_not_empty))

    def back(self):
        previous_move = self.history.pop()
        self.grid[previous_move[0], previous_move[1]] = 0

    def win(self):

        for row in range(self.length):
            counter_p1=0
            counter_p2=0
            for col in range(self.height):
                if self.grid[row,col] == 1:
                    counter_p1 += 1
                    counter_p2 = 0
                    if counter_p1 == 4:
                        return 1
                elif self.grid[row,col] == 2:
                    counter_p1 = 0
                    counter_p2 += 1
                    if counter_p2 == 4:
                        return 2
                else:
                    counter_p1=0
                    counter_p2=0
                    
        for col in range(self.height):
            counter_p1=0
            counter_p2=0
            for row in range(self.length):
                if self.grid[row,col] == 1:
                    counter_p1 += 1
                    counter_p2 = 0
                    if counter_p1 == 4:
                        return 1
                elif self.grid[row,col] == 2:
                    counter_p1 = 0
                    counter_p2 += 1
                    if counter_p2 == 4:
                        return 2
                else:
                    counter_p1=0
                    counter_p2=0
        
        nb_diag = self.height + self.length - 7
        for dgd in range(nb_diag):
            
            counter_p1 = 0
            counter_p2 = 0
            nb_cells_dg = min(self.length, self.height, 4 + dgd, nb_diag - dgd + 3)
            col_0 = max(0, self.height - 4 - dgd)
            row_0 = max(0, dgd - self.height + 4)
            for i in range(nb_cells_dg):
                if self.grid[row_0 + i, col_0 + i] == 1:
                    counter_p1 += 1
                    counter_p2 = 0
                    if counter_p1 == 4:
                        return 1
                elif self.grid[row_0 + i, col_0 + i] == 2:
                    counter_p1 = 0
                    counter_p2 += 1
                    if counter_p2 == 4:
                        return 2
                else:
                    counter_p1 = 0
                    counter_p2 = 0
        
        for dga in range(nb_diag):
            counter_p1 = 0
            counter_p2 = 0
            nb_cells_dg = min(self.length, self.height, 4 + dga, nb_diag - dga + 3)
            row_0 = min(self.length - 1, 3 + dga)
            col_0 = max(0, dga - self.length + 4)
            
            for i in range(nb_cells_dg):
                if self.grid[row_0 - i, col_0 + i] == 1:
                    counter_p1 += 1
                    counter_p2 = 0
                    if counter_p1 == 4:
                        return 1
                elif self.grid[row_0 - i, col_0 + i] == 2:
                    counter_p1 = 0
                    counter_p2 += 1
                    if counter_p2 == 4:
                        return 2
                else:
                    counter_p1 = 0
                    counter_p2 = 0
                
        return "no winner"
    
    def random_play(self, seed=123):
        np.random.seed(seed)
        counter = 0
        while self.win() == "no winner":
            player = counter % 2 + 1
            self.random_move(self, player)
            counter += 1
        return self.win()
    
    def random_move(self, player):
        if not (self.grid[:,-1]==0).any():
            raise Exception("grid full")
        valid_cols = np.argwhere(self.grid[:,-1]==0)
        random_col = np.random.choice(valid_cols.flatten())
        return self.turn(player, random_col)
    
    def tree(self, max_depth, player):  # root_player
        new_game = fGame()
        assert player == 1 or player == 2
        t_grid = tuple(map(tuple, self.grid))
        current_list = [(t_grid, 0, None, None)]
        the_tree = [current_list]
        for depth in range(max_depth):
            if player == 1:
                player = 2
            else:
                player = 1
            parent_list = current_list
            current_list = []
            for parent in parent_list:
                if parent[1] == 0:
                    for col in range(self.length):
                        if parent[0][col][-1] == 0:
                            new_game.grid = np.array(parent[0])
                            new_game.turn(player, col)
                            winner = new_game.win()
                            t_grid = tuple(map(tuple, new_game.grid))
                            current_list.append((t_grid, winner, parent[0], col))
                            if winner != 0:
                                break
            assert current_list != parent_list
            if current_list == []:
                print("BROKE")
                break
            else:
                the_tree.append(current_list)
        return the_tree

    @staticmethod
    def minmax(my_tree):
        all_moves = set()
        for move in my_tree[1]:
            if move[1] == 1:
                return move[3]  # won
            all_moves.add(move[0])
        losing_moves = set()
        for move in my_tree[2]:
            if move[1] == 2:
                losing_moves.add(move[2])
        not_losing_moves = all_moves - losing_moves
        if not_losing_moves == set():
            return 1  # Lost anyway
        moves_not_played_by_opponent = set()
        for move in my_tree[3]:
            if move[1] == 1:
                moves_not_played_by_opponent.add(move[2])
        situation_to_avoid = set()       
        for move in my_tree[4]:
            situation_to_avoid.add(move[2])
        riposte_to_avoid = set()
        for move in my_tree[3]:
            if move[0] in situation_to_avoid:
                riposte_to_avoid.add(move[2])
        riposte_to_avoid -= moves_not_played_by_opponent  # otherwise we win
        move_to_avoid = set()
        for move in my_tree[2]:
            if move[0] in riposte_to_avoid:
                move_to_avoid.add(move[2])
        moves_to_play = not_losing_moves - move_to_avoid
        if moves_to_play != set():
            the_move = moves_to_play.pop()
            for move in my_tree[1]:
                if move[0] == the_move:
                    return move[3]
        the_move = not_losing_moves.pop()
        for move in my_tree[1]:
                if move[0] == the_move:
                    return move[3]

    def ai_move(self, player):
        if player == 1:
            root_player = 2
        else:
            root_player = 1
        ai_tree = self.tree(4, root_player)
        ai_move = self.minmax(ai_tree)
        print("ai_move :", ai_move)
        self.turn(player, ai_move)


root = Tk()

empty_button = ImageTk.PhotoImage(Image.open("graphics/case_vide.png"))

blue_empty = ImageTk.PhotoImage(Image.open("graphics/blue_empty.png"))
red_circle = ImageTk.PhotoImage(Image.open("graphics/red_circle.png"))
yellow_circle = ImageTk.PhotoImage(Image.open("graphics/yellow_circle.png"))

red_button = ImageTk.PhotoImage(Image.open("graphics/red_button.png"))
yellow_button = ImageTk.PhotoImage(Image.open("graphics/yellow_button.png"))

red_green = ImageTk.PhotoImage(Image.open("graphics/red_green.png"))
yellow_green = ImageTk.PhotoImage(Image.open("graphics/yellow_green.png"))

value_images = {0:blue_empty, 
                1:red_circle, 
                2:yellow_circle}

button_images = {1:red_button,
                 2:yellow_button}

button_green = {1:red_green,
                2:yellow_green}

player_color = {1:"Red",
                2:"Yellow"}

the_game = Game()

global the_player
global playing_random

the_player = 1
playing_random = False


root.title("Connect 4")
root.geometry("400x400")


main_frame = Frame(root)

top_container = Frame(main_frame)
top_container.grid(row=0, column=0)

grid_container = Frame(main_frame)
grid_container.grid(row=1, column=0)

bottom_container = Frame(main_frame)
bottom_container.grid(row=2, column=0)

label_top = Label(top_container, text=player_color[the_player]+" to play")
label_top.config(font=("Courier", 44))
label_top.grid(row=0, column=0)

label_bottom = Label(bottom_container, text="") # Text is added if random play mode is on
label_bottom.config(font=("Courier", 14))
label_bottom.grid(row=0, column=0)

buttons = {}
for i in range(the_game.length):    
    buttons[i] = Button(grid_container, image=button_images[the_player], bd=0)
    buttons[i].grid(row=0, column=i)


enter_buttons = []
exit_buttons = []

for i in range(the_game.length):
    def enter_button(event, button_num=i):
        if buttons[button_num]["state"] == "normal":
            buttons[button_num].configure(image=button_green[the_player])
        else:
            pass
    enter_buttons.append(enter_button)
    
    def exit_button(event, button_num=i):
        if buttons[button_num]["state"] == "normal":
            buttons[button_num].configure(image = button_images[the_player])
        else:
            pass
    exit_buttons.append(exit_button)
    
    



label = {}
for col in range(the_game.length):
    label[col] = {}
    for row in range(the_game.height):
        value = the_game.grid[row, col]
        label[col][row] = Label(grid_container, image=blue_empty, bd=1)
        label[col][row].grid(row=the_game.height+1-row, column=col)
        
        
def restart():
    global the_player
    the_game.clear_grid()
    for i in range(the_game.length):
        buttons[i]["state"] = "normal"
        buttons[i].configure(image=button_images[the_player])
    update(colol=None)
        
def restart_question(winner):
    response = messagebox.askyesno(title="Game end", message=player_color[winner]+" has won\nPlay again ?")

    if response==True:
        restart()
    elif response==False:
        update(colol=None) # root.quit()

def go_back():
    the_game.back()
    update(colol=None)
    for i in range(the_game.length):
        buttons[i]["state"] = "normal"
        buttons[i].configure(image=button_images[the_player])
    
def random_move():
    global the_player
    #the_game.random_move(the_player)
    the_game.ai_move(the_player)
    update(colol=None)
    return 0
    
def random_play():  # switch in menu
    global playing_random
    if playing_random == False:
        playing_random = True
        label_bottom.config(text="Opponent: computer playing randomly")
    else:
        playing_random = False
        label_bottom.config(text="")
    return playing_random

update_functions = []

for i in range(the_game.length):
    
    def update(colol=i):
        global the_player
        global playing_random
        
        the_grid = the_game.turn(player=the_player, row=colol)

        
        for col in range(the_game.length):
            
            for row in range(the_game.height):
                value = the_grid[col, row]
                label[col][row].config(image=value_images[value])
        
        if the_player==1:
            the_player=2
        else:
            the_player=1
            
        if playing_random == True and the_player==2 and the_game.win()!=1:
            random_move()
        
        label_top.config(text=player_color[the_player]+" to play")
        
        for i in range(the_game.length):
            buttons[i].config(image=button_images[the_player])
        
        winner = the_game.win()
        
        if winner==1 or winner==2:
            label_top.config(text=player_color[winner]+" has won")
            for i in range(the_game.length):
                buttons[i]["state"] = "disable"
                buttons[i].configure(image=empty_button)
            #restart_question(winner)
        
    update_functions.append(update)


    
for i in range(the_game.length):
    buttons[i].config(command=update_functions[i])
    buttons[i].bind('<Enter>', enter_buttons[i])
    buttons[i].bind('<Leave>', exit_buttons[i])
    
menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Restart", command=restart)
filemenu.add_command(label="Back", command=go_back)
filemenu.add_command(label="Random move", command=random_move)
filemenu.add_checkbutton(label="Random play", command=random_play)
filemenu.add_command(label="Exit") #, command=root.quit)

menubar.add_cascade(label="Options", menu=filemenu)

root.config(menu=menubar)



main_frame.pack()

root.mainloop()
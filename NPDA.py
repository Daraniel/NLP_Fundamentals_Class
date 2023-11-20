from tkinter import *
from tkinter import simpledialog
import math
from itertools import chain
from collections import defaultdict
import itertools
import string
from tkinter import messagebox
import os
import sys
from tkinter import filedialog

root = Tk()
root.title("NPDA")
frame = Frame(root)
frame.pack()
frame_top_left = Frame(frame, width=300, height=300)
frame_top_left.grid(row=0, column=0)
frame_left = Frame(frame)
frame_left.grid(row=0, column=1)
frame3 = Frame(frame)
frame3.grid(row=1, column=0)
frame4 = Frame(frame)
frame4.grid(row=1, column=1)
ws = root.winfo_screenwidth()
x = (ws/4)
root.geometry("+%d+0" % (x))
root.resizable(False, False)


class NPDA:
    Alphabet = list()
    initial_state = 's'
    final_states = list()
    nodes = {}

    def __init__(self, initial_state, final_states, nodes):
        self.initial_state = initial_state
        self.final_states = final_states
        self.nodes = nodes
        for x in self.nodes:
            for y in nodes[x]:
                if not (y[0] in self.Alphabet):
                    self.Alphabet.append(y[0])

    def __str__(self):
        string = str(self.initial_state + '\n' + ' '.join(self.final_states)) + '\n'
        for x in self.nodes:
            for y in self.nodes[x]:
                if isinstance(y[0], list):
                    string += str(x) + "".join(y[0]) + str(y[1]) + '\n'
                else:
                    string += str(x) + y[0] + str(y[1]) + '\n'
        return string

    def standardize(self):
        final_states = ['f']
        stack_alphabet = ''
        for x in self.Alphabet:
            stack_alphabet = stack_alphabet + ''.join(x[1:])
        stack_alphabet = ''.join(ch for ch, _ in itertools.groupby(''.join(stack_alphabet)))
        nodes = self.nodes.copy()
        for y in list(self.nodes.keys()):
            nodes[y] = [([w[0][0].replace('$', '#'), w[0][1].replace('$', '#'), w[0][2].replace('$', '#')], w[1]) for w in nodes[y]]
        initial_state = 's'
        nodes[initial_state] = [('--$', self.initial_state)]
        for x in list(nodes.keys())[:len(nodes.keys())-1]:
            if x in self.final_states:
                nodes[x] = [*nodes[x], ('---', 'r')]
            if len(nodes[x]) == 0:
                nodes[x] = [('-$$', 't')]
            else:
                nodes[x] = [*nodes[x], ('-$$', 't')]

        temp = nodes.copy()
        nodes = {}
        for x in list(temp.keys()):
            for y in temp[x]:
                if x not in nodes.keys():
                    nodes[x] = [([y[0][0], y[0][1], y[0][2]], y[1])]
                else:
                    nodes[x] = [*nodes[x], ([y[0][0], y[0][1], y[0][2]], y[1])]

        nodes['t'] = []
        nodes['f'] = []
        nodes['r'] = [(['-', '$', '-'], 'f')]
        for x in stack_alphabet:
            if x != '$' and x != '-':
                nodes['r'] = [*nodes['r'], (['-', x, '-'], 'r')]
        counter = 0
        for t in list(nodes.keys()):
            for y in nodes[t]:
                if y[0][1] == '-' and (y[0][2] != '-' and y[0][2] != '$'):
                    for x in stack_alphabet:
                        if x != '$' and x != '-':
                            nodes[t] = [*nodes[t], ([y[0][0], x, str(y[0][2])+x], y[1])]
                    nodes[t].remove(y)
                elif len(y[0][2]) >= 3:
                    for x in stack_alphabet:
                        if x != '$' and x != '-':
                            nodes[str(counter)] = [([y[0][0], x, str(y[0][2][0]) + x], y[1])]
                    counter += 1
                    self.shorten(nodes, t, y[0], stack_alphabet, counter)
                    nodes[t].remove(y)
                elif y[0][2] != '-' and y[0][2] != '$':
                    for x in stack_alphabet:
                        if x != '$' and x != '-':
                            nodes[t] = [*nodes[t], ([y[0][0], y[0][1], x+str(y[0][2])], str(counter))]
                            if str(counter) not in nodes.keys():
                                nodes[str(counter)] = [([y[0][0], x, '-'], y[1])]
                            else:
                                nodes[str(counter)] = [*nodes[str(counter)], ([y[0][0], x, '-'], y[1])]
                    counter += 1
                    nodes[t].remove(y)
        return NPDA(initial_state, final_states, nodes)

    def shorten(self, nodes, t, y, stack_alphabet, counter):
        y[2] = y[2][1:]
        if len(y[2]) >= 3:
            for x in stack_alphabet:
                if x != '$' and x != '-':
                    nodes[str(counter)] = [*nodes[str(counter)], ([y[0], x, str(y[2][0]) + x], str(counter-1))]
            counter += 1
            self.shorten(nodes, t, y[0], stack_alphabet, counter)
            nodes[t].remove(y)
        else:
            nodes[t] = [*nodes[t], (y, str(counter-1))]

    def convert_to_grammar(self):
        grammar = ''
        for x in list(self.nodes.keys()):
            for y in self.nodes[x]:
                if y[0][2] == '-':
                    grammar = grammar + x + y[0][1] + y[1] + '->' + y[0][0] + '\n'
                elif len(y[0][2]) == 2:
                    for j in list(self.nodes.keys()):
                        for l in list(self.nodes.keys()):
                            grammar = grammar + '(' + x + y[0][1] + j + ')->' + y[0][0] + '(' + y[1] + y[0][2][0] + l + ')(' + l + \
                                      y[0][2][1] + j + ')' + '\n'

        return grammar

    def show(self, canvas):
        frame_size = 205
        mid = 100
        length = len(self.nodes)
        for i in range(length):
            for temp in list(self.nodes.values())[i]:
                try:
                    x = list(self.nodes.keys()).index(temp[1])
                except:
                    x = list(self.nodes.keys()).index(temp[1][0][0])
                colors = ['blue', 'cyan', 'orange', 'green', 'teal', 'pink']
                ind = self.Alphabet.index(temp[0])
                while ind >= len(colors):
                    ind -= len(colors)
                if x == i:
                    canvas.create_arc(frame_size + mid * math.cos(math.pi * i / length * 2),
                                      frame_size + mid * math.sin(math.pi * i / length * 2),
                                      frame_size + mid * math.cos(math.pi * i / length * 2) + 30 * (
                                              0.2 * math.copysign(1, math.cos(math.pi * i / length * 2)) + math.cos(
                                          math.pi * i / length * 2)),
                                      frame_size + mid * math.sin(math.pi * i / length * 2) + 30 * (
                                              0.2 * math.copysign(1, math.sin(math.pi * i / length * 2)) + math.sin(
                                          math.pi * i / length * 2)),
                                      extent=180, style=ARC, outline='gray')
                    canvas.create_arc(frame_size + mid * math.cos(math.pi * i / length * 2) + 30 * (
                            0.2 * math.copysign(1, math.cos(math.pi * i / length * 2)) + math.cos(
                        math.pi * i / length * 2)),
                                      frame_size + mid * math.sin(math.pi * i / length * 2) + 30 * (
                                              0.2 * math.copysign(1, math.sin(math.pi * i / length * 2)) + math.sin(
                                          math.pi * i / length * 2)),
                                      frame_size + mid * math.cos(math.pi * i / length * 2),
                                      frame_size + mid * math.sin(math.pi * i / length * 2),
                                      extent=-180, style=ARC, outline='gray')
                    canvas.create_text(frame_size + mid * math.cos(math.pi * i / length * 2) + 30 * (
                            0.2 * ind * math.copysign(1, math.cos(math.pi * i / length * 2)) + math.cos(
                        math.pi * i / length * 2)),
                                       frame_size + mid * math.sin(math.pi * i / length * 2) + 30 * (
                                               0.2 * ind * math.copysign(1, math.sin(
                                           math.pi * i / length * 2)) + math.sin(math.pi * i / length * 2)),
                                       fill=colors[ind], font="Times 12 italic bold",
                                       text=temp[0])
                else:
                    canvas.create_line(frame_size + mid * math.cos(math.pi * i / length * 2),
                                       frame_size + mid * math.sin(math.pi * i / length * 2),
                                       (frame_size + mid * math.cos(
                                           math.pi * i / length * 2) + frame_size + mid * math.cos(
                                           math.pi * x / length * 2)) / 2,
                                       (frame_size + mid * math.sin(
                                           math.pi * i / length * 2) + frame_size + mid * math.sin(
                                           math.pi * x / length * 2)) / 2,
                                       fill='gray', arrow=LAST)
                    canvas.create_line(
                        (frame_size + mid * math.cos(math.pi * i / length * 2) + frame_size + mid * math.cos(
                            math.pi * x / length * 2)) / 2,
                        (frame_size + mid * math.sin(math.pi * i / length * 2) + frame_size + mid * math.sin(
                            math.pi * x / length * 2)) / 2,
                        frame_size + mid * math.cos(math.pi * x / length * 2),
                        frame_size + mid * math.sin(math.pi * x / length * 2),
                        fill='gray')
                    if math.cos(math.pi * i / length * 2) > math.cos(math.pi * x / length * 2):
                        s = 5
                    else:
                        s = -5
                    if math.sin(math.pi * i / length * 2) > math.sin(math.pi * x / length * 2):
                        k = 5
                    else:
                        k = -5
                    canvas.create_text(
                        s * ind + (frame_size + mid * math.cos(math.pi * i / length * 2) + frame_size + mid * math.cos(
                            math.pi * x / length * 2)) / 2,
                        k * ind + (frame_size + mid * math.sin(math.pi * i / length * 2) + frame_size + mid * math.sin(
                            math.pi * x / length * 2)) / 2,
                        fill=colors[ind], font="Times 12 italic bold",
                        text=temp[0])
            for j in range(length):
                app.circle(canvas, frame_size + mid * math.cos(math.pi * j / length * 2),
                           frame_size + mid * math.sin(math.pi * j / length * 2), 17.5)
                # print(list(self.nodes.keys())[j])
                if str(list(self.nodes.keys())[j]) in self.final_states:
                    app.circle(canvas, frame_size + mid * math.cos(math.pi * j / length * 2),
                               frame_size + mid * math.sin(math.pi * j / length * 2), 15.5)
                canvas.create_text(frame_size + mid * math.cos(math.pi * j / length * 2),
                                   frame_size + mid * math.sin(math.pi * j / length * 2),
                                   fill="black", font="Times 12 italic bold",
                                   text=list(self.nodes.keys())[j])
                if str(list(self.nodes.keys())[j]) in self.initial_state:
                    canvas.create_line(frame_size + mid * math.cos(math.pi * j / length * 2) + 30 * (
                            0.2 * math.copysign(1, math.cos(math.pi * j / length * 2)) + math.cos(
                        math.pi * j / length * 2)),
                                       frame_size + mid * math.sin(math.pi * j / length * 2) + 30 * (
                                               0.2 * math.copysign(1, math.sin(math.pi * j / length * 2)) + math.sin(
                                           math.pi * j / length * 2)),
                                       frame_size + mid * math.cos(math.pi * j / length * 2),
                                       frame_size + mid * math.sin(math.pi * j / length * 2),
                                       fill='gray', arrow=LAST)


def create_machine(path_to_file):
    file = open(path_to_file, 'r')
    initial_state = file.readline()
    initial_state = initial_state[:len(initial_state) - 1]
    final_states = file.readline().split()
    nodes = {}
    for line in file:
        if line[0] in nodes:
            nodes[line[0]] = [*(nodes[line[0]]), ([line[1], line[2], line[3:len(line)-2]], line[len(line)-2])]
        else:
            nodes[line[0]] = [([line[1], line[2], line[3:len(line)-2]], line[len(line)-2])]
    if not (initial_state in nodes):
        nodes[initial_state] = {}
    for i in final_states:
        if not (i in nodes):
            nodes[i] = {}
    for i in list(nodes.values()):
        if i:
            for j in i:
                if j[1] not in list(nodes.keys()):
                    nodes[j[1]] = {}
    return NPDA(initial_state, final_states, nodes)


# gui to draw the graph
class Gui:
    @staticmethod
    def qui():
        try:
            global app
            tmp = open(app.filename, 'w')
            tmp.close()
            os.remove(app.filename)
        except:
            messagebox.showinfo('failed to delete temp file!\n please delete it manually!')
        root.destroy()

    def __init__(self):
        self.filename = 'temp9856245306546temp.txt'
        try:
            os.remove(self.filename)
        except:
            pass
        self.canvas_left = Canvas(frame_left, width=360, height=335)
        self.canvas_left.pack(fill=BOTH, expand=1)
        self.label_left = Label(frame_left, text="NPDA")
        self.label_left.pack()
        self.canvas3 = Canvas(frame3, width=360, height=335)
        self.canvas3.pack(fill=BOTH, expand=1)
        self.label3 = Label(frame3, text="Standardized NPDA")
        self.label3.pack()
        self.label_grammar0 = Label(frame4, font="DEFAULT 8")
        self.label_grammar1 = Label(frame4, font="DEFAULT 8")
        self.label_grammar2 = Label(frame4, font="DEFAULT 8")
        self.label_grammar3 = Label(frame4, font="DEFAULT 8")
        self.label_grammar4 = Label(frame4, font="DEFAULT 8")
        self.label_grammar5 = Label(frame4, font="DEFAULT 8")
        self.label_grammar6 = Label(frame4, font="DEFAULT 8")
        self.label_grammar7 = Label(frame4, font="DEFAULT 8")
        self.disc = Label(frame_top_left, text="use click to add states and transitions. use right click to mark the final states.")
        self.disc.pack()
        self.canvas = Canvas(frame_top_left, width=250, height=250, highlightbackground="black")
        self.canvas.bind('<ButtonRelease-1>', self.button_released)
        self.canvas.bind('<ButtonRelease-3>', self.button_released2)
        self.canvas.pack(pady=5)
        self.check = 0
        self.states = []
        self.final_states = []
        self.trans = []
        self.temp = (0, 0)
        self.index = 0
        self.frame = Frame(frame_top_left)
        self.frame.pack()
        self.label = Label(self.frame, text="when buttons are disabled reset the program")
        self.label.grid(row=0, column=0, columnspan=4)
        self.button = Button(self.frame, command=self.get_input, text='generate grammar')
        self.button.grid(row=1, column=0)
        self.button2 = Button(self.frame, command=self.reset, text="reset")
        self.button2.grid(row=1, column=1, padx=5)
        self.button3 = Button(self.frame, command=self.open_file, text="open file")
        self.button3.grid(row=1, column=2)
        self.button4 = Button(self.frame, command=self.save_fie, text="save to file")
        self.button4.grid(row=1, column=3)
        self.button4.config(state="disabled")
        self.standard = IntVar()
        Checkbutton(self.frame, text="convert to standard npda", onvalue=1, offvalue=0,
                    variable=self.standard).grid(row=3, column=1, columnspan=4, sticky=W)

    @staticmethod
    def circle(canvas, center_x, center_y, radius):
        canvas.create_oval(center_x - radius, center_y - radius,
                           center_x + radius, center_y + radius,
                           width=1.25, fill='red')

    def button_released(self, event):
        (x, y) = (event.x, event.y)
        a = list(set(range(x - 17, x + 17)).intersection([z[1] for z in self.states]))
        b = list(set(range(x - 25, x + 25)).intersection([z[1] for z in self.states]))
        if a:
            if not set(range(y - 17, y + 17)).isdisjoint([z[2] for z in self.states if z[1] in a]):
                if self.check == 0:
                    self.check = 1
                    self.temp = (x, y)
                else:
                    self.check = 0
                    text1 = ''
                    chars = set('qwertyuiopasdfghjklzxcvbnm$-')
                    chars2 = set('qwertyuiopasdfghjklzxcvbnm$')
                    while True:
                        text1 = simpledialog.askstring("Input", "Please enter transition", parent=root)
                        if text1 is None:
                            return
                        if len(text1) > 2 and not any(c not in chars for c in text1[:2]) and text1[0] != '$':
                            if len(text1) > 3 and not any(c not in chars2 for c in text1[2:]):
                                break
                            elif len(text1) == 3 and not any(c not in chars for c in text1[2:]):
                                break
                    self.canvas.create_line(self.temp[0], self.temp[1], x, y, fill='gray', arrow=LAST)
                    self.canvas.create_text((self.temp[0] + x) / 2, (self.temp[1] + y) / 2, fill='black', font="Times 12 italic bold", text=text1)
                    for e in self.states:
                        if e[1] in range(self.temp[0] - 17, self.temp[0] + 17):
                            if e[2] in range(self.temp[1] - 17, self.temp[1] + 17):
                                for q in self.states:
                                    if q[1] in range(x - 17, x + 17):
                                        if q[2] in range(y - 17, y + 17):
                                            self.trans.append(e[0]+text1+q[0])
            elif b and not set(range(y - 25, y + 25)).isdisjoint([z[2] for z in self.states if z[1] in b]):
                self.check = 0
            else:
                self.circle(self.canvas, x, y, 17.5)
                self.canvas.create_text(x, y, text=(string.ascii_uppercase[self.index]))
                self.states.append((string.ascii_uppercase[self.index], x, y))
                self.index += 1
        elif b and not set(range(y - 25, y + 25)).isdisjoint([z[2] for z in self.states if z[1] in b]):
            self.check = 0
        else:
            self.check = 0
            self.circle(self.canvas, x, y, 17.5)
            self.canvas.create_text(x, y, text=(string.ascii_uppercase[self.index]))
            self.states.append((string.ascii_uppercase[self.index], x, y))
            self.index += 1

    def button_released2(self, event):
        self.check = 0
        (x, y) = (event.x, event.y)
        for e in self.states:
            if e[1] in range(x - 17, x + 17):
                if e[2] in range(y - 17, y + 17):
                    self.final_states.append(e[0]+' ')
                    self.circle(self.canvas, e[1], e[2], 15.5)
                    self.canvas.create_text(e[1], e[2], text=e[0])
                    break

    def get_input(self):
        if len(self.final_states) == 0:
            messagebox.showinfo("Error", "Invalid NFA! \nPlease add the final states!")
            return
        if len(self.trans) == 0:
            messagebox.showinfo("Error", "Invalid NFA! \nPlease add some transitions")
            return
        try:
            tmp = open(self.filename, 'a')
            tmp.writelines(str(self.states[0][0]) + '\n' + ''.join(self.final_states) + '\n' + '\n'.join(self.trans) + '\n')
            tmp.close()
            global app
            self.npda = create_machine(self.filename)
            self.npda.show(app.canvas_left)
            if self.standard.get():
                self.standard_npda = self.npda.standardize()
                self.standard_npda.show(app.canvas3)
                txt = self.standard_npda.convert_to_grammar()
            else:
                txt = self.npda.convert_to_grammar()
            max_lines = 30
            if txt.count('\n') > max_lines:
                if txt.count('\n') > max_lines*2:
                    if txt.count('\n') > max_lines*3:
                        if txt.count('\n') > max_lines * 4:
                            if txt.count('\n') > max_lines * 5:
                                if txt.count('\n') > max_lines * 6:
                                    if txt.count('\n') > max_lines * 7:
                                        txt = txt.split('\n')
                                        self.label_grammar0.config(text='\n'.join(txt[:max_lines]))
                                        self.label_grammar1.config(text='\n'.join(txt[max_lines:max_lines * 2]))
                                        self.label_grammar2.config(text='\n'.join(txt[max_lines * 2:max_lines * 3]))
                                        self.label_grammar3.config(text='\n'.join(txt[max_lines * 3:max_lines * 4]))
                                        self.label_grammar4.config(text='\n'.join(txt[max_lines * 4::max_lines * 5]))
                                        self.label_grammar5.config(text='\n'.join(txt[max_lines * 5::max_lines * 6]))
                                        self.label_grammar6.config(text='\n'.join(txt[max_lines * 6::max_lines * 7]))
                                        self.label_grammar7.config(text='\n'.join(txt[max_lines * 7:]))
                                        self.label_grammar0.grid(row=0, column=0)
                                        self.label_grammar1.grid(row=0, column=1)
                                        self.label_grammar2.grid(row=0, column=2)
                                        self.label_grammar3.grid(row=0, column=3)
                                        self.label_grammar4.grid(row=0, column=4)
                                        self.label_grammar5.grid(row=0, column=5)
                                        self.label_grammar6.grid(row=0, column=6)
                                        self.label_grammar7.grid(row=0, column=7)
                                    else:
                                        txt = txt.split('\n')
                                        self.label_grammar0.config(text='\n'.join(txt[:max_lines]))
                                        self.label_grammar1.config(text='\n'.join(txt[max_lines:max_lines * 2]))
                                        self.label_grammar2.config(text='\n'.join(txt[max_lines * 2:max_lines * 3]))
                                        self.label_grammar3.config(text='\n'.join(txt[max_lines * 3:max_lines * 4]))
                                        self.label_grammar4.config(text='\n'.join(txt[max_lines * 4::max_lines * 5]))
                                        self.label_grammar5.config(text='\n'.join(txt[max_lines * 5::max_lines * 6]))
                                        self.label_grammar6.config(text='\n'.join(txt[max_lines * 6:]))
                                        self.label_grammar0.grid(row=0, column=0)
                                        self.label_grammar1.grid(row=0, column=1)
                                        self.label_grammar2.grid(row=0, column=2)
                                        self.label_grammar3.grid(row=0, column=3)
                                        self.label_grammar4.grid(row=0, column=4)
                                        self.label_grammar5.grid(row=0, column=5)
                                        self.label_grammar6.grid(row=0, column=6)
                                else:
                                    txt = txt.split('\n')
                                    self.label_grammar0.config(text='\n'.join(txt[:max_lines]))
                                    self.label_grammar1.config(text='\n'.join(txt[max_lines:max_lines * 2]))
                                    self.label_grammar2.config(text='\n'.join(txt[max_lines * 2:max_lines * 3]))
                                    self.label_grammar3.config(text='\n'.join(txt[max_lines * 3:max_lines * 4]))
                                    self.label_grammar4.config(text='\n'.join(txt[max_lines * 4::max_lines * 5]))
                                    self.label_grammar5.config(text='\n'.join(txt[max_lines * 5:]))
                                    self.label_grammar0.grid(row=0, column=0)
                                    self.label_grammar1.grid(row=0, column=1)
                                    self.label_grammar2.grid(row=0, column=2)
                                    self.label_grammar3.grid(row=0, column=3)
                                    self.label_grammar4.grid(row=0, column=4)
                                    self.label_grammar5.grid(row=0, column=5)
                            else:
                                txt = txt.split('\n')
                                self.label_grammar0.config(text='\n'.join(txt[:max_lines]))
                                self.label_grammar1.config(text='\n'.join(txt[max_lines:max_lines*2]))
                                self.label_grammar2.config(text='\n'.join(txt[max_lines*2:max_lines*3]))
                                self.label_grammar3.config(text='\n'.join(txt[max_lines*3:max_lines*4]))
                                self.label_grammar4.config(text='\n'.join(txt[max_lines*4:]))
                                self.label_grammar0.grid(row=0, column=0)
                                self.label_grammar1.grid(row=0, column=1)
                                self.label_grammar2.grid(row=0, column=2)
                                self.label_grammar3.grid(row=0, column=3)
                                self.label_grammar4.grid(row=0, column=4)
                        else:
                            txt = txt.split('\n')
                            self.label_grammar0.config(text='\n'.join(txt[:max_lines]))
                            self.label_grammar1.config(text='\n'.join(txt[max_lines:max_lines*2]))
                            self.label_grammar2.config(text='\n'.join(txt[max_lines*2:max_lines*3]))
                            self.label_grammar3.config(text='\n'.join(txt[max_lines*3:]))
                            self.label_grammar0.grid(row=0, column=0)
                            self.label_grammar1.grid(row=0, column=1)
                            self.label_grammar2.grid(row=0, column=2)
                            self.label_grammar3.grid(row=0, column=3)
                    else:
                        txt = txt.split('\n')
                        self.label_grammar0.config(text='\n'.join(txt[:max_lines]))
                        self.label_grammar1.config(text='\n'.join(txt[max_lines:max_lines*2]))
                        self.label_grammar2.config(text='\n'.join(txt[max_lines*2:]))
                        self.label_grammar0.grid(row=0, column=0)
                        self.label_grammar1.grid(row=0, column=1)
                        self.label_grammar2.grid(row=0, column=2)
                else:
                    txt = txt.split('\n')
                    self.label_grammar0.config(text='\n'.join(txt[:max_lines]))
                    self.label_grammar1.config(text='\n'.join(txt[max_lines:]))
                    self.label_grammar0.grid(row=0, column=0)
                    self.label_grammar1.grid(row=0, column=1)

            else:
                self.label_grammar0.config(text=txt)
                self.label_grammar0.grid(row=0, column=0)
            self.button.config(state="disabled")
            self.button3.config(state="disabled")
            self.button4.config(state="normal")
        except:
            messagebox.showinfo("Error", "Invalid NFA!")

    @staticmethod
    def reset():
        app.qui()
        python = sys.executable
        os.execl(python, 'NPDA.py', *sys.argv)

    def open_file(self):
        file = filedialog.askopenfilename(title="Please select file",
                                          filetypes=(("text files", "*.txt"), ("all files", "*.*")))

        try:
            self.npda = create_machine(file)
            self.npda.show(app.canvas_left)
            if self.standard.get():
                self.standard_npda = self.npda.standardize()
                self.standard_npda.show(app.canvas3)
                txt = self.standard_npda.convert_to_grammar()
            else:
                txt = self.npda.convert_to_grammar()
            max_lines = 30
            if txt.count('\n') > max_lines:
                if txt.count('\n') > max_lines * 2:
                    if txt.count('\n') > max_lines * 3:
                        if txt.count('\n') > max_lines * 4:
                            if txt.count('\n') > max_lines * 5:
                                if txt.count('\n') > max_lines * 6:
                                    if txt.count('\n') > max_lines * 7:
                                        txt = txt.split('\n')
                                        self.label_grammar0.config(text='\n'.join(txt[:max_lines]))
                                        self.label_grammar1.config(text='\n'.join(txt[max_lines:max_lines * 2]))
                                        self.label_grammar2.config(text='\n'.join(txt[max_lines * 2:max_lines * 3]))
                                        self.label_grammar3.config(text='\n'.join(txt[max_lines * 3:max_lines * 4]))
                                        self.label_grammar4.config(text='\n'.join(txt[max_lines * 4::max_lines * 5]))
                                        self.label_grammar5.config(text='\n'.join(txt[max_lines * 5::max_lines * 6]))
                                        self.label_grammar6.config(text='\n'.join(txt[max_lines * 6::max_lines * 7]))
                                        self.label_grammar7.config(text='\n'.join(txt[max_lines * 7:]))
                                        self.label_grammar0.grid(row=0, column=0)
                                        self.label_grammar1.grid(row=0, column=1)
                                        self.label_grammar2.grid(row=0, column=2)
                                        self.label_grammar3.grid(row=0, column=3)
                                        self.label_grammar4.grid(row=0, column=4)
                                        self.label_grammar5.grid(row=0, column=5)
                                        self.label_grammar6.grid(row=0, column=6)
                                        self.label_grammar7.grid(row=0, column=7)
                                    else:
                                        txt = txt.split('\n')
                                        self.label_grammar0.config(text='\n'.join(txt[:max_lines]))
                                        self.label_grammar1.config(text='\n'.join(txt[max_lines:max_lines * 2]))
                                        self.label_grammar2.config(text='\n'.join(txt[max_lines * 2:max_lines * 3]))
                                        self.label_grammar3.config(text='\n'.join(txt[max_lines * 3:max_lines * 4]))
                                        self.label_grammar4.config(text='\n'.join(txt[max_lines * 4::max_lines * 5]))
                                        self.label_grammar5.config(text='\n'.join(txt[max_lines * 5::max_lines * 6]))
                                        self.label_grammar6.config(text='\n'.join(txt[max_lines * 6:]))
                                        self.label_grammar0.grid(row=0, column=0)
                                        self.label_grammar1.grid(row=0, column=1)
                                        self.label_grammar2.grid(row=0, column=2)
                                        self.label_grammar3.grid(row=0, column=3)
                                        self.label_grammar4.grid(row=0, column=4)
                                        self.label_grammar5.grid(row=0, column=5)
                                        self.label_grammar6.grid(row=0, column=6)
                                else:
                                    txt = txt.split('\n')
                                    self.label_grammar0.config(text='\n'.join(txt[:max_lines]))
                                    self.label_grammar1.config(text='\n'.join(txt[max_lines:max_lines * 2]))
                                    self.label_grammar2.config(text='\n'.join(txt[max_lines * 2:max_lines * 3]))
                                    self.label_grammar3.config(text='\n'.join(txt[max_lines * 3:max_lines * 4]))
                                    self.label_grammar4.config(text='\n'.join(txt[max_lines * 4::max_lines * 5]))
                                    self.label_grammar5.config(text='\n'.join(txt[max_lines * 5:]))
                                    self.label_grammar0.grid(row=0, column=0)
                                    self.label_grammar1.grid(row=0, column=1)
                                    self.label_grammar2.grid(row=0, column=2)
                                    self.label_grammar3.grid(row=0, column=3)
                                    self.label_grammar4.grid(row=0, column=4)
                                    self.label_grammar5.grid(row=0, column=5)
                            else:
                                txt = txt.split('\n')
                                self.label_grammar0.config(text='\n'.join(txt[:max_lines]))
                                self.label_grammar1.config(text='\n'.join(txt[max_lines:max_lines * 2]))
                                self.label_grammar2.config(text='\n'.join(txt[max_lines * 2:max_lines * 3]))
                                self.label_grammar3.config(text='\n'.join(txt[max_lines * 3:max_lines * 4]))
                                self.label_grammar4.config(text='\n'.join(txt[max_lines * 4:]))
                                self.label_grammar0.grid(row=0, column=0)
                                self.label_grammar1.grid(row=0, column=1)
                                self.label_grammar2.grid(row=0, column=2)
                                self.label_grammar3.grid(row=0, column=3)
                                self.label_grammar4.grid(row=0, column=4)
                        else:
                            txt = txt.split('\n')
                            self.label_grammar0.config(text='\n'.join(txt[:max_lines]))
                            self.label_grammar1.config(text='\n'.join(txt[max_lines:max_lines * 2]))
                            self.label_grammar2.config(text='\n'.join(txt[max_lines * 2:max_lines * 3]))
                            self.label_grammar3.config(text='\n'.join(txt[max_lines * 3:]))
                            self.label_grammar0.grid(row=0, column=0)
                            self.label_grammar1.grid(row=0, column=1)
                            self.label_grammar2.grid(row=0, column=2)
                            self.label_grammar3.grid(row=0, column=3)
                    else:
                        txt = txt.split('\n')
                        self.label_grammar0.config(text='\n'.join(txt[:max_lines]))
                        self.label_grammar1.config(text='\n'.join(txt[max_lines:max_lines * 2]))
                        self.label_grammar2.config(text='\n'.join(txt[max_lines * 2:]))
                        self.label_grammar0.grid(row=0, column=0)
                        self.label_grammar1.grid(row=0, column=1)
                        self.label_grammar2.grid(row=0, column=2)
                else:
                    txt = txt.split('\n')
                    self.label_grammar0.config(text='\n'.join(txt[:max_lines]))
                    self.label_grammar1.config(text='\n'.join(txt[max_lines:]))
                    self.label_grammar0.grid(row=0, column=0)
                    self.label_grammar1.grid(row=0, column=1)

            else:
                self.label_grammar0.config(text=txt)
                self.label_grammar0.grid(row=0, column=0)
            self.button.config(state="disabled")
            self.button3.config(state="disabled")
            self.button4.config(state="normal")
        except:
            messagebox.showinfo("Error", "Invalid File! \nPlease check if file exists and has correct format")

    def save_fie(self):
        file0 = filedialog.asksaveasfilename(title="Please select npda file", filetypes=(("text files", "*.txt"), ("all files", "*.*")))
        file0 = open(file0, 'w')
        file0.writelines(str(self.npda))
        file0.close()

        if self.standard.get():
            file1 = filedialog.asksaveasfilename(title="Please select standard npda file",
                                                 filetypes=(("text files", "*.txt"), ("all files", "*.*")))
            file1 = open(file1, 'w')
            file1.writelines(str(self.standard_npda))
            file1.close()

        file2 = filedialog.asksaveasfilename(title="Please select grammar file",
                                             filetypes=(("text files", "*.txt"), ("all files", "*.*")))
        file2 = open(file2, 'w')
        file2.writelines(str(self.label_grammar.cget("text")))
        file2.close()


app = Gui()
root.protocol('WM_DELETE_WINDOW', Gui.qui)
root.mainloop()

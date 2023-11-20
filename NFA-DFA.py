from tkinter import *
from tkinter import simpledialog
import math
from itertools import chain
from collections import defaultdict
import string
from tkinter import messagebox
import os
import sys
from tkinter import filedialog

root = Tk()
root.title("Finite Automaton")
frame = Frame(root)
frame.pack()
frame_top_left = Frame(frame, width=300, height=300, )
frame_top_left.grid(row=0, column=0)
frame_top_right = Frame(frame, width=300, height=300, )
frame_top_right.grid(row=0, column=1)
frame_left = Frame(frame)
frame_left.grid(row=1, column=0)
frame_right = Frame(frame)
frame_right.grid(row=1, column=1)
ws = root.winfo_screenwidth()
x = (ws/4)
root.geometry("+%d+0" % (x))
root.resizable(False, False)


class FiniteAutomaton:
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
                string += str(x) + y[0] + str(y[1]) + '\n'
        return string

    def show(self, canvas):
        frame_size = 210
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
                                                  0.2 * math.copysign(1, math.cos(math.pi * j / length * 2)) + math.cos(math.pi * j / length * 2)),
                                       frame_size + mid * math.sin(math.pi * j / length * 2) + 30 * (
                                                  0.2 * math.copysign(1, math.sin(math.pi * j / length * 2)) + math.sin(math.pi * j / length * 2)),
                                       frame_size + mid * math.cos(math.pi * j / length * 2),
                                       frame_size + mid * math.sin(math.pi * j / length * 2),
                                       fill='gray', arrow=LAST)


class DFA(FiniteAutomaton):
    def simplify(self):
        check = ['0'] * len(self.nodes.keys())
        for x in self.nodes.keys():
            if x in self.final_states or str(x) in self.final_states:
                check[list(self.nodes.keys()).index(x)] = '2'
            else:
                check[list(self.nodes.keys()).index(x)] = '1'
        prev = check.copy()
        for x in self.nodes.keys():
            for y in self.Alphabet:
                chk = 0
                for z in self.nodes[x]:
                    if z[0] == y:
                        chk = prev[list(self.nodes.keys()).index(anti_none(z[1]))]
                        break
                check[list(self.nodes.keys()).index(x)] = str(check[list(self.nodes.keys()).index(x)]) + str(chk)
        while True:
            prev = check.copy()
            for x in self.nodes.keys():
                for y in self.Alphabet:
                    chk = 0
                    for z in self.nodes[x]:
                        if z[0] == y:
                            chk = prev[list(self.nodes.keys()).index(anti_none(z[1]))]
                            break
                    check[list(self.nodes.keys()).index(x)] = str(check[list(self.nodes.keys()).index(x)]) + str(chk)
            chk = 0
            for x in check:
                for y in check:
                    if x == y:
                        if prev[check.index(x)] != prev[check.index(y)]:
                            chk = 1
                    else:
                        if prev[check.index(x)] == prev[check.index(y)]:
                            chk = 1
            if chk == 0:
                break
        set_check = list(set(check))
        chk = [0] * len(set_check)
        nodes = {}
        index = 0
        final_states = ''
        for x in check:
            if chk[set_check.index(x)] == 0:
                chk[set_check.index(x)] = 1
                if x[0] == '2':
                    final_states = final_states + string.ascii_uppercase[set_check.index(x)]
                for z in self.nodes[list(self.nodes.keys())[check.index(x)]]:
                    if string.ascii_uppercase[set_check.index(x)] in nodes.keys():
                        # if isinstance(nodes[string.ascii_uppercase[set_check.index(x)]][0], tuple):
                        nodes[string.ascii_uppercase[set_check.index(x)]] = [*(nodes[string.ascii_uppercase[set_check.index(x)]]), (z[0], string.ascii_uppercase[set_check.index(check[list(self.nodes.keys()).index(anti_none(z[1]))])])]
                        # else:
                        #     nodes[string.ascii_uppercase[set_check.index(x)]] = (nodes[string.ascii_uppercase[set_check.index(x)]], (z[0], string.ascii_uppercase[set_check.index(check[list(self.nodes.keys()).index(anti_none(z[1]))])]))
                    else:
                        nodes[string.ascii_uppercase[set_check.index(x)]] = [(z[0], string.ascii_uppercase[set_check.index(check[list(self.nodes.keys()).index(anti_none(z[1]))])])]
        index += 1
        return DFA(list(nodes.keys())[0], final_states, nodes)


class NFA(FiniteAutomaton):
    # lambda is mapped to -
    def nfa_to_dfa(self, state=None, nodes={}):
        if state is None:
            lamb = 0
            check = 0
            state = anti_none(self.anti_lambda(self.initial_state))
            if state != self.initial_state:
                lamb = 1
            final_states = self.final_states.copy()
        elif state in nodes:
            return nodes[state]
        else:
            check = 1
        trans = {}
        try:
            for x in list(self.nodes[state]):
                if x[0] == '-':
                    if x[0] not in trans:
                        trans[x[0]] = x[1]
                    else:
                        trans[x[0]] = anti_none([*(trans[x[0]]), self.anti_lambda(x[1])])
                    if len(trans) == 1:
                        trans = self.get_trans(x[1])
                    else:
                        trans = anti_none([*(trans), self.get_trans(x[1])])
                elif x[0] in trans:  # list(self.nodes.values())[i]
                    trans[x[0]] = [*(trans[x[0]]), x[1]]
                else:
                    trans[x[0]] = x[1]
            pass

        except Exception as e:
            for x in state:
                if x in nodes and state in nodes.keys() and nodes[state] is not None:
                    m = self.nfa_to_dfa(x, nodes)
                    if m is not None and m not in nodes[state] and m != nodes[state]:
                        # nodes[str(trans[x])] = nodes[str(trans[x])] + self.nfa_to_dfa(y, nodes)
                        dict3 = defaultdict(list)
                        for k, v in chain(nodes[state], m):
                            dict3[k].append(v)
                        nodes[state] = [(v, tuple(k)) for v, k in dict3.items()]
                else:
                    if check == 0 and lamb == 1 and state in nodes.keys():
                        if state in nodes.keys():
                            pass
                    else:
                        nodes[state] = (self.nfa_to_dfa(x, nodes))
                    pass
            my_list2 = list(nodes[state])
            for q in nodes[state]:
                r = q
                for w in q[1]:
                    for e in q[1]:
                        try:
                            if w in e and e not in w:
                                my_list = list(q[1])
                                my_list.remove(w)
                                if len(my_list) == 1:
                                    r = my_list[0]
                                else:
                                    r = tuple(xi for xi in my_list if xi is not None)
                                my_list2[my_list2.index(q)] = (q[0], r)
                        except:
                            pass
                nodes[state] = tuple(my_list2)
                pass
            if check == 1:
                return nodes[state]

        for x in trans:
            if isinstance(trans[x], list):
                trans[x].sort()
                trans[x] = tuple(trans[x])
        if check == 1:
            nodes[state] = trans.items()
        else:
            if lamb == 0:
                nodes[state] = trans.items()
            else:
                if len(trans) != 0:
                    nodes[state] += trans
        for x in trans:
            for y in trans[x]:
                if trans[x] in nodes and nodes[trans[x]] is not None:
                    m = self.nfa_to_dfa(y, nodes)
                    if m is not None and m not in nodes[trans[x]] and m != nodes[trans[x]]:
                        # nodes[str(trans[x])] = nodes[str(trans[x])] + self.nfa_to_dfa(y, nodes)
                        dict3 = defaultdict(list)
                        for k, v in chain(nodes[trans[x]], m):
                            dict3[k].append(v)

                        dd = defaultdict(list)
                        l = {}
                        for n in nodes[trans[x]]:
                            l[n[0]] = n[1]
                        p = {}
                        for u in m:
                            p[u[0]] = u[1]
                        for d in (l, p):
                            for key, value in d.items():
                                if ((isinstance(dd[key], tuple) or isinstance(dd[key], list)) and len(
                                        dd[key]) != 0) or isinstance(value, tuple) or isinstance(value, list):
                                    if value not in dd[key]:
                                        dd[key].append(value)
                                        if len(dd[key]) > 1:
                                            if isinstance(dd[key][0], str):
                                                if isinstance(dd[key][1], str):
                                                    pass
                                                else:
                                                    if dd[key][0] in dd[key][1]:
                                                        dd[key] = tuple(dd[key][1])
                                                    else:
                                                        dd[key] = tuple(dd[key][0]) + dd[key][1]
                                            elif isinstance(dd[key][1], str):
                                                if dd[key][1] in dd[key][0]:
                                                    dd[key] = tuple(dd[key][0])
                                                else:
                                                    dd[key] = dd[key][0] + tuple(dd[key][1])
                                            else:
                                                dd[key] = dd[key][0] + dd[key][1]
                                else:
                                    dd[key].append(tuple(value))
                        nodes[trans[x]] = [(v, tuple(k)) for v, k in dd.items()]
                        # nodes[trans[x]] = [(v, tuple(k)) for v, k in dict3.items()]
                else:
                    nodes[trans[x]] = (self.nfa_to_dfa(y, nodes))
        if check == 1:
            return nodes[state]
        else:
            for x in list(nodes.values()):
                for y in x:
                    nodes[y[1]] = self.nfa_to_dfa(y[1], nodes)

            if '-' in self.Alphabet:
                index = self.Alphabet.index('-')
                self.Alphabet = self.Alphabet[:index] + self.Alphabet[index + 1:]
            nodes['t'] = [(x, 't') for x in self.Alphabet]
            for x in list(nodes.keys()):
                for z in final_states:
                    if z in x and x not in final_states:
                        final_states.append(str(x))
                    if not (isinstance(z, str)):
                        for u in x:
                            if z in u and u not in final_states:
                                final_states.append(str(u))
                if nodes[x] is None:
                    nodes[x] = [(self.Alphabet[0], 't')]
                if len(nodes[x]) == 1:
                    nodes[x] = nodes[x]
                else:
                    nodes[x] = tuple([*(nodes[x])])
                for u in self.Alphabet:
                    tmp = 0
                    for k in nodes[x]:
                        if u in [k][0]:
                            tmp = 1
                    if tmp == 0:
                        nodes[x] = [*(nodes[x]), (u, 't')]
            for x in list(nodes.keys()):
                m = anti_none(nodes[x])
                nodes[x] = m
                if isinstance(nodes[x], tuple):
                    if isinstance(nodes[x][0], str):
                        nodes[x] = [nodes[x]]
                    else:
                        nodes[x] = [*nodes[x]]
            for x in list(nodes.keys()):
                if isinstance(x, tuple) and len(x) == 2 and x[1] is None:
                    tmp = nodes[x]
                    nodes.pop(x, None)
                    nodes[x] = x[0]
            for x in list(nodes.keys()):
                if (x,) in nodes:
                    nodes.pop((x,), None)
            for x in list(nodes.keys()):
                try:
                    for y in nodes[x]:
                        if y[0] == '-':
                            nodes = poper(y[1], nodes)
                            temp = []
                            for u in nodes[x]:
                                if u != y:
                                    if len(temp) == 0:
                                        temp = [u]
                                    else:
                                        temp = [*(temp), u]
                            nodes[x] = temp
                            break
                except:
                    pass
            for x in list(nodes.keys()):
                if x not in final_states:
                    try:
                        for y in self.nodes[x]:
                            if y[0] == '-':
                                if y[1] in final_states:
                                    final_states.append(x)
                                else:
                                    try:
                                        for u in self.nodes[y[1]]:
                                            if u[0] == '-':
                                                if u[1] in final_states:
                                                    final_states.append(x)
                                        else:
                                            try:
                                                for z in self.nodes[u[1]]:
                                                    if z[0] == '-':
                                                        if z[1] in final_states:
                                                            final_states.append(x)
                                            except:
                                                pass
                                    except:
                                        pass
                    except:
                        pass

            check = [0] * len(nodes.keys())
            check = self.anti_extra(self.initial_state, nodes, check)
            dict2 = nodes.copy()

            for x in dict2:
                if check[list(dict2.keys()).index(x)] == 0:
                    nodes.pop(x, None)

            return DFA(self.initial_state, final_states, nodes)

    def anti_extra(self, node, nodes, check):
        if check[list(nodes.keys()).index(node)] == 1:
            return check
        check[list(nodes.keys()).index(node)] = 1
        for x in nodes[node]:
            check = self.anti_extra(anti_none(x[1]), nodes, check)
        return check

    def get_trans(self, node):
        trans = {}
        for x in self.nodes[node]:
            if x[0] in trans.keys():  # trans[0]:  # list(self.nodes.values())[i]
                trans[x[0]] = [*(trans[x[0]]), x[1]]
            else:
                trans[x[0]] = x[1]
            if x[0] == '-':
                m = self.get_trans(x[1])
                if len(m) != 0:
                    if m is not None and m != trans:
                        dict3 = defaultdict(list)
                        for k, v in chain(trans.items(), m.items()):
                            dict3[k].append(v)
                        trans = dict3
        return trans

    def anti_lambda(self, state=None, prev_states=[]):
        check = 1
        if state is None:
            check = 0
            state = self.initial_state
        new_state = state
        if new_state in prev_states:
            return prev_states[prev_states.index(new_state)]
        elif isinstance(state, tuple) or isinstance(state, list):
            for i in state:
                new_state = [*(new_state), self.anti_lambda(i, prev_states)]
                prev_states.append(new_state)
                return tuple(new_state)
        for i in self.nodes[state]:
            if i[0] == '-':
                new_state = [*(new_state), self.anti_lambda(i[1], prev_states)]
        if new_state not in prev_states:
            prev_states.append(new_state)
        return anti_none(tuple(new_state))


def anti_none(x):
    try:
        if (x[0] >= 'a' and x[0] <= 'z') or x[0] == '-':
            return (x[0], anti_none(x[1]))
    except:
        pass
    if isinstance(x, list) or isinstance(x, tuple):
        if len(x) >= 1:
            if (isinstance(x, tuple) or isinstance(x, list)) and len(x[0]) > 1:
                z = list()
                for y in x:
                    z.append(anti_none(y))
                if len(z) > 1 and z[len(z) - 1] is not None:
                    z = tuple(z)
                if len(z) == 1:
                    z = z[0]
                else:
                    if z[len(z) - 2] is None:
                        z = z[len(z) - 2]
                    else:
                        z = z
                for r in z:
                    if len(r) != 1:
                        for t in r[1:][0]:
                            for q in r[1:][0]:
                                try:
                                    if q in t and q != t:
                                        ls = list(z)
                                        ls[z.index(r)] = (r[0], t)
                                        z = tuple(ls)
                                except:
                                    pass
                return z
        if x[len(x) - 1] is None:
            if len(x) == 2:
                x = x[0]
            else:
                x = tuple(x[:len(x) - 2])
        elif len(x) > 1:
            return x
        else:
            x = x[0]
    return x


def poper(z, nodes):
    if z not in nodes.keys():
        nodes.pop(z, None)
        return nodes
    for x in list(nodes[z]):
        for y in nodes[x[1]]:
            if y[0] == '-':
                nodes = poper(y[1], nodes)
                nodes.pop(x, None)
                break
    nodes.pop(z, None)
    return nodes


def create_machine(path_to_file):
    file = open(path_to_file, 'r')
    initial_state = file.readline()
    initial_state = initial_state[:len(initial_state) - 1]
    final_states = file.readline().split()
    # final_states = final_states[:len(final_states) - 1]
    nodes = {}
    for line in file:
        if line[0] in nodes:
            nodes[line[0]] = [*(nodes[line[0]]), (line[1], line[2])]
        else:
            nodes[line[0]] = [(line[1], line[2])]
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
    return NFA(initial_state, final_states, nodes)


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
        self.canvas_left = Canvas(frame_left, width=360, height=360)
        self.canvas_left.pack(fill=BOTH, expand=1)
        self.label_left = Label(frame_left, text="NFA")
        self.label_left.pack()
        self.canvas_right = Canvas(frame_right, width=360, height=360)
        self.canvas_right.pack(fill=BOTH, expand=1)
        self.label_right = Label(frame_right, text="DFA")
        self.label_right.pack()
        self.canvas_top_right = Canvas(frame_top_right, width=360, height=360)
        self.canvas_top_right.pack(fill=BOTH, expand=1)
        self.label_top_right = Label(frame_top_right, text="Simplified DFA")
        self.label_top_right.pack()
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
        self.button = Button(self.frame, command=self.get_input, text='generate NFA')
        self.button.grid(row=1, column=0)
        self.button2 = Button(self.frame, command=self.reset, text="reset")
        self.button2.grid(row=1, column=1, padx=5)
        self.button3 = Button(self.frame, command=self.open_file, text="open file")
        self.button3.grid(row=1, column=2)
        self.button4 = Button(self.frame, command=self.save_fie, text="save to file")
        self.button4.grid(row=1, column=3)
        self.button4.config(state="disabled")

    @staticmethod
    def circle(canvas, center_x, center_y, radius):
        canvas.create_oval(center_x - radius, center_y - radius,
                           center_x + radius, center_y + radius,
                           width=1.25, fill='red')

    def button_released(self, event):
        (x, y) = (event.x, event.y)
        if not set(range(x - 17, x + 17)).isdisjoint([z[1] for z in self.states]):
            if not set(range(y - 17, y + 17)).isdisjoint([z[2] for z in self.states]):
                if self.check == 0:
                    self.check = 1
                    self.temp = (x, y)
                else:
                    self.check = 0
                    text1 = ''
                    while len(text1) != 1 or (text1 > 'z' or text1 < 'a') and text1 != '-':
                        text1 = simpledialog.askstring("Input", "Please enter transition", parent=root)
                        if text1 is None:
                            return
                    self.canvas.create_line(self.temp[0], self.temp[1], x, y, fill='gray', arrow=LAST)
                    self.canvas.create_text((self.temp[0] + x) / 2, (self.temp[1] + y) / 2, fill='black', font="Times 12 italic bold", text=text1)
                    for e in self.states:
                        if e[1] in range(self.temp[0] - 17, self.temp[0] + 17):
                            if e[2] in range(self.temp[1] - 17, self.temp[1] + 17):
                                for q in self.states:
                                    if q[1] in range(x - 17, x + 17):
                                        if q[2] in range(y - 17, y + 17):
                                            self.trans.append(e[0]+text1+q[0])
            else:
                self.circle(self.canvas, x, y, 17.5)
                self.canvas.create_text(x, y, text=(string.ascii_uppercase[self.index]))
                self.states.append((string.ascii_uppercase[self.index], x, y))
                self.index += 1
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
            tmp.writelines(str(self.states[0][0]) + '\n' + ''.join(self.final_states) + '\n' + '\n'.join(self.trans))
            tmp.close()
            global app
            self.nfa = create_machine(self.filename)
            app.canvas_left.delete('all')
            self.nfa.show(app.canvas_left)
            app.canvas_right.delete('all')
            self.dfa = self.nfa.nfa_to_dfa()
            self.dfa.show(app.canvas_right)
            self.simplified_dfa = self.dfa.simplify()
            self.simplified_dfa.show(app.canvas_top_right)
            self.button.config(state="disabled")
            self.button3.config(state="disabled")
            self.button4.config(state="normal")
        except:
            messagebox.showinfo("Error", "Invalid NFA!")

    @staticmethod
    def reset():
        app.qui()
        python = sys.executable
        os.execl(python, 'NFA-DFA.py', *sys.argv)

    def open_file(self):
        file = filedialog.askopenfilename(title="Please select file",
                                          filetypes=(("text files", "*.txt"), ("all files", "*.*")))

        try:
            self.nfa = create_machine(file)
            self.nfa.show(app.canvas_left)
            self.dfa = self.nfa.nfa_to_dfa()
            self.dfa.show(app.canvas_right)
            self.simplified_dfa = self.dfa.simplify()
            self.simplified_dfa.show(app.canvas_top_right)
            self.button.config(state="disabled")
            self.button3.config(state="disabled")
            self.button4.config(state="normal")
        except:
            messagebox.showinfo("Error", "Invalid File! \nPlease check if file exists and has correct format")

    def save_fie(self):
        file0 = filedialog.asksaveasfilename(title="Please select nfa file", filetypes=(("text files", "*.txt"), ("all files", "*.*")))
        file0 = open(file0, 'w')
        file0.writelines(str(self.nfa))
        file0.close()
        file1 = filedialog.asksaveasfilename(title="Please select dfa file", filetypes=(("text files", "*.txt"), ("all files", "*.*")))
        file1 = open(file1, 'w')
        file1.writelines(str(self.dfa))
        file1.close()
        file2 = filedialog.asksaveasfilename(title="Please select simplified dfa file", filetypes=(("text files", "*.txt"), ("all files", "*.*")))
        file2 = open(file2, 'w')
        file2.writelines(str(self.simplified_dfa))
        file2.close()


app = Gui()
root.protocol('WM_DELETE_WINDOW', Gui.qui)
root.mainloop()

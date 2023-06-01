import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os


class FindTruthTable:
    def __init__(self,eq: str = None) -> None:
        self.eq = eq
        
        self.content = []
        self.x = 0
        
        for i in eq:
            if i.isalpha() and i not in self.content:
                self.content.append(i)
                self.x+=1
        self.content = sorted(self.content)
        
    def infixToPostfix(self): 
        Operators = set(['+', '-', '*', '/', '(', ')'])  # collection of Operators
        Priority = {'+':1, '-':1, '*':2, '/':2,}
        stack = [] # initialization of empty stack
        output = '' 

        for character in self.eq:
            if character not in Operators:  # if an operand append in postfix expression
                output+= character
            elif character=='(':  # else Operators push onto stack
                stack.append('(')
            elif character==')':        
                while stack and stack[-1]!= '(':
                    output+=stack.pop()
                stack.pop()
            else: 
                while stack and stack[-1]!='(' and Priority[character]<=Priority[stack[-1]]:
                    output+=stack.pop()
                stack.append(character)
        while stack:
            output+=stack.pop()
        self.eq = output
    
    def signfix(self):
        q = 0
        out = ''
        t = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKKLMNOPQRSTUVWXYZ"
        for i in range(len(self.eq)):
            if self.eq[i] == " ":
                continue
            elif self.eq[i] =="'" or self.eq[i] =="’":
                out+="'"
            elif self.eq[i] in t and  q == 1:
                out+='*'+self.eq[i]
            
            elif self.eq[i] in t:
                out+=self.eq[i]
                q = 1
            elif self.eq[i] == ")":
                out+=self.eq[i]
            elif self.eq[i] =="(" and q == 1:
                out+='*('
                q = 0
            
            elif self.eq[i] not in t:
                out+=self.eq[i]
                q = 0
        self.eq = out
            
    def gate(self, op:str, a:int, b:int = None ) ->int : 
        out = False
        if op == '*':
            out = a & b
        elif op == '+':
            out =  a | b
        elif op == "'":
            out = not a
        
        if out == False:
            return 0
        else:
            return 1
            
    def binary(self,dec: int) -> str:
        out = ''
        q = dec
        r = ''
        while q > 1 :
            r+= str(q%2)
            q = (q//2)
        r+= str(q)

        for i in range(1,len(r)+1):
            out+= r[-i]
            
        out = '0'*(self.x-len(out))+out
        return out
        
    def solvebit(self,bin):
        dic = {}
        for i in range(len(self.content)):
            dic[self.content[i]] = int(bin[i])
        
        stack = []
        for i in range(len(self.eq)):

            if self.eq[i].isalpha():
                stack.append(dic[self.eq[i]])
                
            else:
                if self.eq[i] == "'":
                    k = self.gate(self.eq[i],stack[-1])
                    stack[-1] = k
                else:
                    k = self.gate(self.eq[i],stack[-1],stack[-2])
                    del stack[-1]
                    stack[-1] = k

        return stack[-1]
        
    def solve (self) -> str:
        try:
            self.signfix()
            self.infixToPostfix()
            out = 'dec '
            mean = []
            t = '|___'*(self.x+1)
            for i in range(len(self.content)):
                
                
                if (i+1)%self.x == 0:
                    out+=(f'| {self.content[i]} | --> Output\n{t}|___________\n')
                else:
                    out+=(f'| {self.content[i]} ')
            for j in range(2**self.x):
                bin = self.binary(j)
                sol = self.solvebit(bin)
                if sol == 1:
                    mean.append(j)
                out+="{:<4}".format(j)
                for i in range(len(bin)):
                    if (i+1)%self.x == 0:
                        out+=(f'| {bin[i]} | -->  {sol}\n')
                    else:
                        out+=(f'| {bin[i]} ')
            out+=(f'Min terms: {mean}')
            return out
        except:
            return "You might have provided an incorrect expression."


def run_code():
    text = ""
    text += "Expression: {}\n".format(name.get())
    a = FindTruthTable(name.get())
    text+= a.solve()
    

    resp = messagebox.askquestion(title="Validity", message=f"Shall I start running with the following expression?\n\nExpression: {name.get()}")
    if resp == 'yes':
        
        output_window['state'] = 'normal'  # allow editing of the Text widget    
        output_window.insert('end', f"{text}\n---- Program Ended ----\n\n")
        output_window['state'] = 'disabled'  # disable editing
        output_window.see('end')  # scroll to the end as we make progress
        app.update()


def close_app():
    app.destroy()



app = tk.Tk()
app.title('Truth Table')
# menubar = tk.Menu(app,background='#18191a',foreground='white')
# app.config(menu=menubar)
app['background'] = '#18191a'
# menu1 = tk.Menu(menubar, tearoff=0)
# menubar.add_cascade(label="File", underline=0, menu=menu1)
# menu1.add_separator()
# menu1.add_command(label="Exit", underline=1, command=close_app)

top_frame = tk.Frame(app,background='#18191a')
top_frame.pack(side="top")
pw_frame = tk.Frame(app,background='#18191a')
pw_frame.pack(side="top")

# Simple Label widget:
ex = tk.Label(top_frame, text="Example:", width=7, anchor="w",background='#18191a', foreground= 'white')
ex.pack({"side": "left"})

# Simple Entry widget:
ex_ = tk.Label(top_frame, text="a'bc+a(b+c)'+cd", width=20, anchor="w",background='#18191a', foreground= 'white')
ex_.pack({"side": "left"})

name_title = tk.Label(pw_frame, text="Expression:", width=10, anchor="w",background='#18191a', foreground= 'white')
name_title.pack({"side": "left"})

# Simple Entry widget:
name = tk.Entry(pw_frame, background='#18191a', foreground= 'white')
name.pack({"side": "left"})
# name.insert(0, "Your name")

output_frame = tk.Frame(app)
output_frame.pack()

output_window = tk.Text(output_frame, state='disabled',foreground= 'white',)
output_window['background'] = '#18191a'
output_window.pack()




buttons = tk.Frame(app)
buttons.pack()


action_button = tk.Button(buttons, text="Run", command=run_code, foreground= 'white', background='#18191a')
action_button.pack()

app.mainloop()

import tkinter as tk
import sys
class ConstraintVar:

    def __init__(self, d, n ):
        self.domain = [ v for v in d ]
        self.name = n
        self.neighbors = []

class BinaryConstraint:

    def __init__(self, v1, v2, op,a,fn=None):
        self.var1 = v1
        self.var2 = v2
        self.op = op
        self.a = a
        if fn==None:
            self.func = lambda x,y: ops[op](x,y) == eval(a)
            if(op=='-' or op =='/'):
                self.func = lambda x,y: ( abs(ops[op](x,y)) == eval(a) or abs(ops[op](y,x) ==eval(a)))
        else:
            self.func = fn
    def __str__(self):
        return self.var1.name +self.op+self.var2.name+"  "+self.a

class UnaryConstraint:

    def __init__(self, v, a):
        self.var1 = v
        self.a =a
        self.func = lambda x: x == eval(a)
    def __str__(self):
        return self.var1.name +"= "+self.a

class N_queens:
    def __init__(self,n):
        self.n = n

    def allDiff( self, constraints, v ):

        fn = lambda x,y : x!=y
        for i in v:
            for j in v:
                if ( i != j ) :
                    constraints.append(BinaryConstraint( i,j,'!=','other',fn=fn))

    def setup_diag(self,constraints,v):
        fn = lambda x,y,Qx,Qy : abs(x-y) != abs(Qx-Qy)
        for i in v:
            for j in v:
                if(i!=j):
                    constraints.append(BinaryConstraint(i,j, 'diag','other', fn=fn))

    def revise(self,bc,dom1,dom2,dom3,dom4):

        if isinstance(bc,UnaryConstraint):
            return bc.func(dom1)
        elif isinstance(bc, BinaryConstraint):
            try:
                return bc.func(dom1,dom2,int(bc.var1.name), int(bc.var2.name))
            except:
                return bc.func(dom1,dom2)

        return False

    def check_correct(self, Cs,assignment,Xs):

        inf ={}
        sat = False
        for bc in Cs:
            if isinstance(bc,UnaryConstraint):
                dom1 =  assignment.get(bc.var1.name)
                dom2 = 0
                dom3 = 0
                dom4 =0
            elif isinstance(bc,BinaryConstraint):
                dom1 = assignment.get(bc.var1.name)
                dom2 = assignment.get(bc.var2.name)
                dom3 = 0
                dom4 = 0

            if (dom1 != None and dom2 != None and dom3!=None and dom4!=None):
                if not self.revise(bc,dom1,dom2,dom3,dom4):
                    return  False

        return True

    def MRV(self, assignment,X,constraints):
        max_assigned = -1000
        min_x =''
        for c in constraints:
            count = 0
            if isinstance(c,BinaryConstraint):
                count_var1 = 1 if c.var1.name in assignment else 0
                count_var2 = 1 if c.var2.name in assignment else 0
                sum_count  = count_var1 + count_var2
                if (sum_count) > max_assigned and sum_count <2:
                    max_assigned = count_var1 + count_var2
                    min_x = c.var1.name if count_var1==0 else (c.var2.name if count_var2 == 0 else '')
        if(min_x == ''):
            return list(X.keys())[0]
        return min_x

    def backtrack(self,assignment,C,X):
        if len(assignment)==len(X):
            return True

        var = self.MRV(assignment,X,C)
        for value in X[var]:
            assignment[var]=value
            sat = self.check_correct(C,assignment,X)
            if sat :
                res = self.backtrack(assignment,C,X)
                if res:
                    return True

            del assignment[var]
        return False

    def setUpNqueens(self):
        cols =[str(i) for i in range(1,self.n+1)]
        variables = dict()
        for var in cols:
            variables[var] = ConstraintVar( [i for i in range(1,self.n+1)],var )
        constraints =[]
        var_list = list(variables.values())
        self.allDiff(constraints, var_list)
        self.setup_diag(constraints,var_list)

        var_domain_dict = {}
        for k in variables.keys():
            var_domain_dict.update({k:[i for i in range(1,self.n+1)]})
        return constraints,var_domain_dict

    def printDomains( self,vars, n=4 ):
        count = 0
        for k in sorted(vars.keys()):
            print( k,'{',vars[k],'}, ',end="" )
            count = count+1
            if ( 0 == count % n ):
                print(' ')

    def main(self):
        C,X = self.setUpNqueens()
        assignments = {}
        self.backtrack(assignments,C,X)
        self.printDomains(assignments,n=self.n)
        return assignments

class GUI(tk.Frame):

    def __init__(self, parent, size=8):
        '''size is the size of a square, in pixels'''

        self.rows = size
        self.columns = size
        self.size = 64
        self.color1 = "gold"
        self.color2 = "brown"
        self.pieces = {}

        canvas_width = self.columns * self.size
        canvas_height = self.rows * self.size

        tk.Frame.__init__(self, parent)
        self.canvas = tk.Canvas(self, borderwidth=0, highlightthickness=0,
                                width=canvas_width, height=canvas_height, background="bisque")
        self.canvas.pack(side="top", fill="both", expand=True, padx=2, pady=2)

        # this binding will cause a refresh if the user interactively
        # changes the window size
        self.canvas.bind("<Configure>", self.refresh)

    def addpiece(self, name, image, row=0, column=0):
        '''Add a piece to the playing board'''
        self.canvas.create_image(0,0, image=image, tags=(name, "piece"), anchor="c")
        self.placepiece(name, row, column)

    def placepiece(self, name, row, column):
        '''Place a piece at the given row/column'''
        self.pieces[name] = (row, column)
        x0 = (column * self.size) + int(self.size/2)
        y0 = (row * self.size) + int(self.size/2)
        self.canvas.coords(name, x0, y0)

    def refresh(self, event):
        '''Redraw the board, possibly in response to window being resized'''
        xsize = int((event.width-1) / self.columns)
        ysize = int((event.height-1) / self.rows)
        self.size = min(xsize, ysize)
        self.canvas.delete("square")
        color = self.color2
        for row in range(self.rows):
            color = self.color1 if color == self.color2 else self.color2
            for col in range(self.columns):
                if self.columns%2==1 and col % self.columns==0 :
                    color = self.color1 if color == self.color2 else self.color2
                x1 = (col * self.size)
                y1 = (row * self.size)
                x2 = x1 + self.size
                y2 = y1 + self.size
                self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill=color, tags="square")
                color = self.color1 if color == self.color2 else self.color2
        for name in self.pieces:
            self.placepiece(name, self.pieces[name][0], self.pieces[name][1])
        self.canvas.tag_raise("piece")
        self.canvas.tag_lower("square")   

def main():
    

    if len (sys.argv) != 2:
        print("Usage: python3 nqueens_csp.py n")
        print("n is the number of queens")
        exit(1)
    n = int( sys.argv[1] )
    root = tk.Tk()
    imagedata = 'R0lGODlhKAAoANUAABUVFRAQECgoKFpaWoaGho+Pj3t7e5iYmHBwcKmpqVJSUri4uAAAAC8vL729vRoaGgwMDEpKSsLCwtT \
                 U1KCgoOHh4ejo6MjIyK6urs7Ozjg4OEFBQQMCA9zc3KysrKWlpbKxsfj4+PHx8QgICLS0tGFhYQYGBvr6+WdnZ+/v79jY2OTk5P\
                 b29uvr6v7+/t/f3/3+/vz8++7u7vT09AQEBPv7+wMEAwEBAf38/SEhIf///////wAAAAAAAAAAAAAAACH5BAEAADsALAAAAAAoACgAAAb\
                 /wJ1wSCwaj8ikcslsOp/QqHRKFSYiDcQxMWgoElWrQHHIaYvYg0YR3h0eM53hYRyRdBJAewEgZDQbRgIDEyU5bTsEAQEmSAyLiE\
                 I5OQELRgUBABqROyMfGw1GAQgGeoiYKgkmGEQGASoYjU8oOQBnQ10yJwIRRAADOhl9aBA5BUUUDxQUAcdDOQo6OgcjljsGEBc6ImNECs\
                 0oARREAxHSDQNEHAbSM9BCY9I6EQJEvCJ5zkJ8ywDjQxA8yDsAwU02HTB0IDiE6wEBFAWLIAAQgEEgIQQeTJDXIocGaDh0hGBxwNSOAjkY\
                 AHigr8gBEwwc7hggIIS8aQxoSBCZooWD/2YzR6gEsWQDAAUQIvy6qWPFgwghaqSwUGFCDgEaAmgYcUvJCAJ8GBBgqqMACB1TK6hQEYGBgAMb\
                 6jUZkKNChQELyJ5gIYJqhwkZEChwQIBDyyUmxsY4wdTFib4V/ma44KCyBjpPSghoQdZFiLSSL0hwIKGAYSgLGOTtHKLviwmiHSxYM\
                 CAiFDMx5Im48IGAAQMECnxwQHkBhRy9ohhowKLCAQUCAEDgwOGGDQgAkBv4YNqAFAIANix6oIAABQwLMBwgUKJBAOzRCUg5EEAAggUrZK\
                 xY8aJyhtEkUICAUW9JkQAABSDklwQEYGUWCRh4sEACGggARhQJPBCAAhJY8HSXAQyECAEBICSAgQECcNDAhVDQZ5EEVWVAwkQCbOeBiQakVKB\
                 yCHYQmmgffABhAkQmQME33kWBQAMWeAhYbAuAEKEHVHoAQkldOfFAAwX4ZgACCKBQQgkDlGmmmQ2EEgUHk7Tp5ptuCvAADZzUaeedeN4ZBAA7'

    board = GUI(root, n)
    board.pack(side="top", fill="both", expand="true", padx=4, pady=4)
    q_image = tk.PhotoImage(data=imagedata)

    problem = N_queens(n)
    assignment = problem.main()
    for key in assignment.keys():
        board.addpiece( "p"+key, q_image, int(key)-1, int(assignment[key])-1)

    root.mainloop()

main()

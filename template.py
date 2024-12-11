import copy

# Exercise 1 - Spacemon Competition
"""1.while competition not end(not reach the end of list for each team), minus stamina based on formula alternatively.
If one of the opponent is defeated, increase traversing index by 1 for that team. Repeat the prcocess till one team reaches the end."""
def exercise1(roster1,roster2):
    multi={('Mercury','Mercury'):1,('Mercury','Venus'):2,('Mercury','Earth'):1, ('Mercury','Mars'):0.5, \
           ('Venus','Venus'):1,('Venus','Mercury'):0.5,('Venus','Earth'):2,('Venus','Mars'):1,\
           ('Earth','Earth'):1,('Earth','Mercury'):1,('Earth','Venus'):0.5,('Earth','Mars'):2,\
           ('Mars','Mars'):1, ('Mars','Mercury'):2,('Mars','Venus'):1,('Mars','Earth'):0.5}
    t1=len(roster1)
    t2=len(roster2)
    i,j=0,0
    spacemon_1,spacemon_2=list(roster1[i]),list(roster2[j])
    while i<t1 or j <t2:
        
        
        attack,defence=spacemon_1,spacemon_2
        
        while spacemon_1[1]>0 and spacemon_2[1]>0:
            
            defence[1]-=attack[2]*multi[(attack[0],defence[0])]
            attack,defence=defence,attack
        if spacemon_1[1]<=0:
            i+=1
            if i==t1:
                return False
            spacemon_1=list(roster1[i])
        else:
            j+=1
            if j==t2:
                return True
            spacemon_2=list(roster2[j])
                
    
    
    

# Exercise 2 - Five Letter Unscramble
""", given a string containing letters,
 returns the number of unique words in wordle.txt that can be obtained by
 rearranging the characters in the string. Each character in s can be used at
 most once."""
"""for every word in wordle.txt, check if each letter can be found in the given string,
if all letters can be found, increase count by 1. """
def rearrange(s,letter_count):
    for c in s:
        if c in letter_count:
            letter_count[c]-=1
    for count in letter_count.values():
        if count>0:
            return False        
    return True
def make_counter(word):
    d={}
    for c in word:
        d[c]=d.setdefault(c,0)+1
    return d
def exercise2(s):
    res=[]
    fin=open('wordle.txt')
    for word in fin:
        word=word.strip()
        letter_count=make_counter(word)
        if rearrange(s,letter_count):
            res.append(word)
    return len(res)    


        
        


# Exercise 3 - Wordle Set
def check_green(green,word):
    for idx in green:
         if word[idx]!=green[idx]:
              return False
    return True
def check_yellow(yellow,d):               
    for letter in yellow:
         if letter not in d:
              return False
         else:
            for wrong_idx in yellow[letter]:
                 if wrong_idx in d[letter]:
                      return False  
                      
    return True

def check_gray(gray,d):
    for letter in gray:
         if letter in d:
              return False
    return True

def make_letter_dict(word):
    d={}
    for c,i in zip(word,range(5)):
           d.setdefault(c,set()).add(i)
    return d

def exercise3(green,yellow,gray):
    res=set()
    fin=open('wordle.txt')
    for word in fin:
        word=word.strip() 
        d=make_letter_dict(word)
        valid=all((check_green(green,word),check_yellow(yellow,d),
                  check_gray(gray,d)))
        if valid:
            res.add(word)
    return len(res)

"""Serach the cell of A and B. For every cell, check if its adjacent cells are X or not.
If not x, proceed to this adjacent cell. Else, check for the other ajacent cell and 
 check if its adjacent cells are X or not. If all adjecent cells are X, we backtrack 
 to previous cell. Repeat these steps until B is reached. If B is reached, store the path to 
 tuple."""
# Exercise 4 - 2D Most Rewarding Shortest Path
def get_adjacent_cells(cell,rows,cols):
    up,down,left,right=None,None,None,None
    if cell[0]!=0:
        up=cell[0]-1,cell[1]
    if cell[0]!=rows-1:
        down=cell[0]+1,cell[1]
    if cell[1]!=0:
        left=cell[0],cell[1]-1
    if cell[1]!=cols-1:
        right=cell[0],cell[1]+1
    adj_cells=[up,down,left,right]
    return adj_cells



def find_path(env,start,end,path,visited,all_paths,rows,cols):
    if start==end:
        path.append(end)
        res=tuple(path)
        print(path)
        all_paths.append(res)
        path.pop()
        
    visited.add(start)
    path.append(start)
    adj_cells=get_adjacent_cells(start,rows,cols)
    for cell in adj_cells:
        if cell and cell not in visited and env[cell[0]][cell[1]]!='X':
            find_path(env,cell,end,path,visited,all_paths,rows,cols)
    path.pop()
    visited.remove(start)

            
def find_cell(env,rows,cols,start,end):
    res=[]
    for i in range(rows):
        for j in range(cols):
            if env[i][j]==start or env[i][j]==end:
                res.append((i,j))
    return res
def get_shortest_rewarding_path(env,paths,max_length):
    reward=0
    length=max_length
    for path in paths:
        count=0
        curr_len=len(path)-1
        for step in path:
            if env[step[0]][step[1]]=='R':
                count+=1
        if curr_len<length:
            length=curr_len
            reward=count
        elif curr_len==length and count>reward:
            reward=count
    return length,reward
             


    
def exercise4(env):
    path=[]
    visited=set()
    all_paths=[]
    rows=len(env)
    cols=len(env[0])
    A,B=find_cell(env,rows,cols,'A','B')
    find_path(env,A,B,path,visited,all_paths,rows,cols)
    print(all_paths)
    res=get_shortest_rewarding_path(env,all_paths,rows*cols)
    return res
    

    
"""Initialize a blank list for storing the number of max cliques each actor exists.
For each actor, find all max cliques that is formed by nodes in its adjacency matrix 
and itself. To achieve this, do the following:
initialize a set representing a max clique which must include that actor. 
Then, for each adjacent node of that actor,
check if it is adjacent to all members in the clique, which is done by accessing the
adjacency lists of all members in the set. If all members are adjacent to the node, 
extend the clique by storing the node to the set and increment the count for that node. 
Else, store the node to a list representing
unused nodes for forming max clique with the current actor.
After traversing the adjacency list of the current actor, append the set to res, which
is a dict of {actor: list of max cliques which include that actor}.
Repeat the process for each node in the list of unused nodes.

"""
# Exercise 5 - Social Network Analysis
def remove_used_nodes(nodes):
    unused_nodes=[]
    for node in nodes:
        if node!=-1:
            unused_nodes.append(node)
    return unused_nodes

def form_max_clique(network,unused_nodes,all_max_cliques):
    max_clique=set()
    adjacent=True
    for neighbor in unused_nodes:
            for member in max_clique:
                if  network[member][neighbor]==0:
                    adjacent=False
                    break
            if adjacent:
                unused_nodes[neighbor]=-1
                max_clique.add(neighbor)
    all_max_cliques.append(max_clique)
    unused_nodes=remove_used_nodes(unused_nodes)
    return unused_nodes
def exercise5(network):
    start=0
    res=[]
    
    for actor in network:
        start+=1
        all_max_cliques=[]
        unused_nodes=[]
        for neighbor in range(start,len(actor)):
            unused_nodes.append(neighbor)
        
        while unused_nodes:
            unused_nodes=form_max_clique(network,unused_nodes,all_max_cliques)
            
                
            #check all max_cliques for each actor for debugging
            print(all_max_cliques)
        res.append(len(all_max_cliques))
    return res

    




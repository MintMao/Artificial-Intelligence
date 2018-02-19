import numpy as np
import os, sys
try:
    from tkinter import *
except ImportError:  #Python 2.x
    PythonVersion = 2
    from Tkinter import *
    from tkFont import Font
    from ttk import *
    from tkMessageBox import *
    import tkFileDialog
else:  #Python 3.x
    PythonVersion = 3
    from tkinter.font import Font
    from tkinter.ttk import *
    from tkinter.messagebox import *

# tags for file
file_tag='train' #train/test
#write the file
fw=open('answer_for_train.txt','a');
# The board size of go game
BOARD_SIZE = 9
COLOR_BLACK=-1
COLOR_WHITE=1
COLOR_NONE=0
POINT_STATE_CHECKED=100
POINT_STATE_UNCHECKED=101
POINT_STATE_NOT_ALIVE=102
POINT_STATE_ALIVE=103
POINT_STATE_EMPYT=104

def read_go(file_name):
  # read from txt file and save as a matrix
  go_arr = np.zeros((BOARD_SIZE, BOARD_SIZE))
  for line in open(file_name):
    line = line.strip()
    lst = line.split()
    row = int(lst[0])
    col = int(lst[1])
    val = int(lst[2])
    go_arr[row, col] = val
  #for i in range(go_arr.shape[0]):
   # for j in range(go_arr.shape[1]):
    #  print (go_arr[i,j]," ",end="");
    #print("\n");

  return go_arr


def plot_go(go_arr, txt='Default'):
  # Visualization of a go matrix
  # First draw a canvas with 9*9 grid
  root = Tk()
  cv = Canvas(root, width=50*(BOARD_SIZE+1), height=50*(BOARD_SIZE+1), bg='#F7DCB4')
  cv.create_text(250,10,text=txt,fill='blue')
  cv.pack(side=LEFT)
  size = 50
  for x in range(BOARD_SIZE):
    cv.create_line(size+x*size, size, size+x*size, size+(BOARD_SIZE-1)*size)
  for y in range(BOARD_SIZE):
    cv.create_line(size, size+y*size, size+(BOARD_SIZE-1)*size, size+size*y)
  # Second draw white and black circles on cross points
  offset = 20
  idx_black = np.argwhere(go_arr == COLOR_BLACK)
  idx_white = np.argwhere(go_arr == COLOR_WHITE)
  len_black = idx_black.shape[0]
  len_white = idx_white.shape[0]
  for i in range(len_black):
    if idx_black[i,0] >= BOARD_SIZE or idx_black[i,1] >= BOARD_SIZE:
      print ('IndexError: index out of range')
      sys.exit(0)
    else:
      new_x = 50*(idx_black[i,1]+1)
      new_y = 50*(idx_black[i,0]+1)
      cv.create_oval(new_x-offset, new_y-offset, new_x+offset, new_y+offset, width=1, fill='black', outline='black')
  for i in range(len_white):
    if idx_white[i,0] >= BOARD_SIZE or idx_white[i,1] >= BOARD_SIZE:
      print ('IndexError: index out of range')
      sys.exit(0)
    else:
      new_x = 50*(idx_white[i,1]+1)
      new_y = 50*(idx_white[i,0]+1)
      cv.create_oval(new_x-offset, new_y-offset, new_x+offset, new_y+offset, width=1, fill='white', outline='white')
  root.mainloop()

#-------------------------------------------------------
# Rule judgement  *need finish
#-------------------------------------------------------
def is_alive(check_state, go_arr, x, y):
  '''
  This function checks whether the point (i,j) and its connected points with the same color are alive, it can only be used for white/black chess only
  Depth-first searching.
  :param check_state: The guard array to verify whether a point is checked
  :param go_arr: chess board
  :param i: x-index of the start point of searching
  :param j: y-index of the start point of searching
  :return: POINT_STATE_CHECKED/POINT_STATE_ALIVE/POINT_STATE_NOT_ALIVE, POINT_STATE_CHECKED=> the start point (i,j) is checked, POINT_STATE_ALIVE=> the point and its linked points with the same color are alive, POINT_STATE_NOT_ALIVE=>the point and its linked points with the same color are dead
  '''

#the slice of the cheeses are not alive
#stack.append(the cheese to check)
#while stack is not empty
 # append the same color cheeses
#    meanwhile if there is qi:if yes then the slice of the cheeses are alive
#this cheese is checked
#pop the statck, regrad i,j as the attributes in the next loop

#return the condition of the slice of the cheeses


  cheeses_condition=POINT_STATE_NOT_ALIVE;
  stack=[];
  elem=(x,y);
  stack.append(elem);
  i=elem[0];
  j=elem[1];
  while len(stack)>0:
        if(i+1<go_arr.shape[0]):
            if go_arr[i+1,j]==go_arr[i,j] and check_state[i+1,j]==POINT_STATE_UNCHECKED:
                stack.append((i+1,j));
            if go_arr[i+1,j]==0:
                 cheeses_condition=POINT_STATE_ALIVE;
        if(j+1<go_arr.shape[1]):
             if go_arr[i,j+1]==go_arr[i,j] and check_state[i,j+1]==POINT_STATE_UNCHECKED:
                stack.append((i,j+1));
             if go_arr[i,j+1]==0:
                cheeses_condition=POINT_STATE_ALIVE;
        if(j-1>=0):
            if go_arr[i,j-1]==go_arr[i,j] and check_state[i,j-1]==POINT_STATE_UNCHECKED:
                stack.append((i,j-1));
            if go_arr[i,j-1]==0:
                cheeses_condition=POINT_STATE_ALIVE;
        if(i-1>=0):
            if go_arr[i-1,j]==go_arr[i,j] and check_state[i-1,j]==POINT_STATE_UNCHECKED:
                stack.append((i-1,j));
            if go_arr[i-1,j]==0:
                 cheeses_condition=POINT_STATE_ALIVE;
        check_state[i,j]=POINT_STATE_CHECKED;
        elem=stack.pop();
        i=elem[0];
        j=elem[1];
  return cheeses_condition;





def go_judege(go_arr):
  '''
  :param go_arr: the numpy array contains the chess board
  :return: whether this chess board fit the go rules in the document
           False => unfit rule
           True => ok
  '''
  is_fit_go_rule = True
  check_state = np.zeros(go_arr.shape)
  check_state[:] = POINT_STATE_EMPYT
  tmp_indx = np.where(go_arr != 0)
  check_state[tmp_indx] = POINT_STATE_UNCHECKED
  for i in range(go_arr.shape[0]):
    for j in range(go_arr.shape[1]):
      if check_state[i, j] == POINT_STATE_UNCHECKED:
        tmp_alive = is_alive(check_state, go_arr,i,j);
        if tmp_alive == POINT_STATE_NOT_ALIVE: # once the go rule is broken, stop the searching and return the state
          is_fit_go_rule = False
          break
      else:
        pass # pass if the point and its lined points are checked
  return is_fit_go_rule

#-------------------------------------------------------
# User strategy  *need finish
#-------------------------------------------------------
def user_step_eat(go_arr):
  '''
  :param go_arr: chessboard
  :return: ans=>where to put one step forward for white chess pieces so that some black chess pieces will be killed; user_arr=> the result chessboard after the step
  '''
  user_arr=[];
  for i in range(go_arr.shape[0]):
      for j in range(go_arr.shape[1]):
          if go_arr[i,j]==0 :
              stack_black_cheeses=[];
              if i+1<go_arr.shape[0] and go_arr[i+1,j]==-1:
                  stack_black_cheeses.append((i+1,j));
              if i-1>=0 and go_arr[i-1,j]==-1:
                  stack_black_cheeses.append((i-1,j));
              if j+1<go_arr.shape[1] and go_arr[i,j+1]==-1:
                  stack_black_cheeses.append((i,j+1));
              if j-1>=0 and go_arr[i,j-1]==-1:
                  stack_black_cheeses.append((i,j-1));
              go_arr[i,j]=1;
              if_can_put=False;
              while len(stack_black_cheeses)>0:
                  #If the slice of black cheeses will die.
                  check_state = np.zeros(go_arr.shape);#重复进栈会死循环
                  elem=stack_black_cheeses.pop();
                  slice_black=[];
                  slice_black.append(elem);
                  black_cheese=[];
                  black_cheese.append(elem);
                  if_is_alive=False;
                  while len(slice_black)>0:
                      elem=slice_black.pop();
                      x = elem[0];
                      y = elem[1];
                      check_state[x,y] = 1;
                      if x+1<go_arr.shape[0]:
                          if go_arr[x+1,y]==-1 and check_state[x+1,y]==0:
                             slice_black.append((x+1,y));
                             black_cheese.append((x+1,y));
                          if go_arr[x+1,y]==0:
                              if_is_alive=True;
                              break;
                      if y+1<go_arr.shape[1]:
                          if go_arr[x,y+1]==-1 and check_state[x,y+1]==0:
                              slice_black.append((x,y+1));
                              black_cheese.append((x,y+1));
                          if go_arr[x,y+1]==0:
                              if_is_alive=True;
                              break;
                      if x-1>=0:
                          if go_arr[x-1,y]==-1 and check_state[x-1,y]==0:
                              slice_black.append((x-1,y));
                              black_cheese.append((x-1,y));
                          if go_arr[x-1,y]==0:
                              if_is_alive=True;
                              break;
                      if y-1>=0:
                          if go_arr[x,y-1]==-1 and check_state[x,y-1]==0:
                              slice_black.append((x,y-1));
                              black_cheese.append((x,y-1));
                          if go_arr[x,y-1]==0:
                              if_is_alive=True;
                              break;
                  if if_is_alive==False:
                      if_can_put=True;
                      user_arr.append((i,j));
                      for k in range(len(black_cheese)):
                          elem=black_cheese.pop();
                          x=elem[0];
                          y=elem[1];
                          go_arr[x,y]=0;
              if if_can_put==False: go_arr[i,j]=0;
  return user_arr;





  pass

def user_setp_possible(go_arr):
  '''
  :param go_arr: chessboard
  :return: ans=> all the possible locations to put one step forward for white chess pieces
  '''
  user_arr=[];

  for i in range(go_arr.shape[0]):
      for j in range(go_arr.shape[1]):
          if go_arr[i,j]==0:
              go_arr[i,j]=1;
              check_state = np.zeros(go_arr.shape);
              check_state[:] = POINT_STATE_UNCHECKED;
              tem_alive=is_alive(check_state,go_arr,i,j);
              if tem_alive==POINT_STATE_ALIVE:
                  user_arr.append((i,j));
                  go_arr[i,j]=0;
              if tem_alive==POINT_STATE_NOT_ALIVE:
                  put=False;
                  if i + 1 < go_arr.shape[0] :
                      if is_alive(check_state,go_arr,i+1,j)==POINT_STATE_NOT_ALIVE and go_arr[i+1,j]==-1:
                          put=True;
                  if i - 1 >= 0 :
                      if is_alive(check_state,go_arr,i-1,j)==POINT_STATE_NOT_ALIVE and go_arr[i-1,j]==-1:
                          put=True;
                  if j + 1 < go_arr.shape[1] :
                      if is_alive(check_state,go_arr,i,j+1)==POINT_STATE_NOT_ALIVE and go_arr[i,j+1]==-1:
                          put=True;
                  if j - 1 >= 0 :
                      if is_alive(check_state,go_arr,i,j-1)==POINT_STATE_NOT_ALIVE and go_arr[i,j-1]==-1:
                          put=True;
                  if put==True:
                     user_arr.append((i,j));
                  go_arr[i,j]=0;
  return  user_arr;




  pass

if __name__ == "__main__":
  chess_rule_monitor = True
  problem_tag="Default"
  ans=[]
  user_arr=np.zeros([0,0])

  # The first problem: rule checking
  problem_tag = "Problem 0: rule checking"
  go_arr = read_go('{}_0.txt'.format(file_tag))
  plot_go(go_arr, problem_tag)
  chess_rule_monitor=go_judege(go_arr)
  print ("{}:{}".format(problem_tag, chess_rule_monitor))
  plot_go(go_arr, '{}=>{}'.format(problem_tag, chess_rule_monitor))
  if chess_rule_monitor==True:
      str_value="train_0\n True\n";
  else:
      str_value="train_0\n False\n";
  fw.write(str_value);
  fw.write("\n");

  problem_tag = "Problem 00: rule checking"
  go_arr = read_go('{}_00.txt'.format(file_tag))
  plot_go(go_arr, problem_tag)
  chess_rule_monitor = go_judege(go_arr)
  print ("{}:{}".format(problem_tag, chess_rule_monitor))
  plot_go(go_arr, '{}=>{}'.format(problem_tag, chess_rule_monitor))
  if chess_rule_monitor==True:
      str_value="train_00\n True\n";
  else:
      str_value="train_00\n False\n";
  fw.write(str_value);
  fw.write("\n");

  # The second~fifth prolbem: forward one step and eat the adverse points on the chessboard
  for i in range(1,5):
    problem_tag = "[train]Problem {}: forward on step:".format(i);
    go_arr = read_go('{}_{}.txt'.format(file_tag, i));
    plot_go(go_arr, problem_tag);
    user_arr=user_step_eat(go_arr);
    chess_rule_monitor = go_judege(go_arr);
    #ans, user_arr = user_step_eat(go_arr) # need finish
    print (problem_tag, user_arr);
    plot_go(go_arr, '{}=>{}'.format(problem_tag, chess_rule_monitor))
    fw.write("{}_{}\n".format("train",i));
    for j in range(len(user_arr)):
        elem=user_arr[j];
        x=int(elem[0]);
        y=int(elem[1]);
        str_value=str(x)+" "+str(y)+"\n";
        fw.write(str_value);
    fw.write("\n");



  # The sixth problem: find all the postion which can place a white chess pieces
  problem_tag = "Problem {}: all possible position".format(5)
  go_arr = read_go('{}_{}.txt'.format(file_tag,5))
  plot_go(go_arr, problem_tag)
  chess_rule_monitor = go_judege(go_arr)
  user_arr=user_setp_possible(go_arr);
  #ans = user_setp_possible(go_arr) # need finish
  print ("{}:{}".format(problem_tag,user_arr ))
  plot_go(go_arr, '{}=>{}'.format(problem_tag, chess_rule_monitor))
  fw.write("train_5\n")
  for j in range(len(user_arr)):
      elem = user_arr[j];
      x = int(elem[0]);
      y = int(elem[1]);
      str_value = str(x) + " " + str(y) + "\n";
      fw.write(str_value);
  fw.write("\n");

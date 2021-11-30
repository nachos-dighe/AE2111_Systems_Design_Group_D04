#There are two methods to get filepath, uses .os and .sys
import sys #seems like an annoying module
sys.path #returns list
sys.path.insert(1, '/path/to/application/app/folder')


import os
abs = os.path.abspath(__file__) #returns entire absolute path 
base = os.path.basename(__file__) #returns path[-1], ie filename
join = os.path.join(__file__, 'path to be added') #joins __file__ + 'path to be added'
real = os.path.realpath(__file__) #nothing useful for now

dirname = os.path.dirname(__file__)
dirname_lst = list(dirname)
dirname_lst[-1] = '4'
dirname = "".join(dirname_lst)
filename = os.path.join(dirname, '\WP4_1 Python')

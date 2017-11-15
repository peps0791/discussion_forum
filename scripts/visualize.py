import mysql.connector
from mysql.connector import errorcode
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt
import redis
import pickle
import json
import sys
from scipy import stats

questionarr = [4,4,1,4,6,2,0,0,2,1,0,0,0,0,1,1,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,2,2,0,1,1,1,1,1,1,1,0,0,1,1,2,0,0,0,3,3,1,2,1,0,2,1,1,0,1,0,0,1,0,1,1,1,1,3,0,0,1,0,0,1,2,0,0,1,0,0,0,0,1,1,1,0,0,1,1,1,0,0,1,1,0,0,1,0,3,1,0,1,0,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0,1,1,1,1,1,2,1,5,1,2,1,1,4,0,11,1,1,1,0,3,2,3,1,2,1,1,2,1,1,1,1,0,0,0,0,0,5,1,3,3,1,0,3,1,1,1,1,1,2,1,1,1,1,1,0,0,0,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,2,2,1,1,1,19,1,0,1,1,0,0,0,0,0,0,2,2,0,0,0,1,0,2,0,1,1,0,0,1,0,1,1,0,0,0,2,0,9,0,0,1,0,1,0,0,0,0,0,0,0,1,1,1,5,0,1,2,1,1,1,5,1,1,2,1,0,0,1,1,1,0,1,0,1,0,1,0,0,0,1,0,1,1,4,2,0,0,0,0,0,0,5,6,0,0,0,0,0,3,0,0,0,2,0,0,0,1,0,0,0,0,0,2,0,0,1,0,0,0,0,0,1,1,1,4,1,1,2,1,1,1,2,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,2,1,1,1,0,0,0,0,2,1,1,2,1,0,0,0,0,1,1,1,1,1,1,1,1,0,2,1,1,1,0,1,1,1,0,0,0,0,3,0,0,0,1,0,4,5,0,4,0,3,0,0,0,1,2,0,0,1,0,0,0,1,1,1,1,1,1,1,1,1,1,0,0,2,2,1,1,0,1,0,1,1,3,1,1,1,2,1,2,2,1,0,0,0,3,3,1,1,2,1,1,1,1,2,2,0,0,1,1,1,1,1,1,0,0,0,0,1,0,0,0,0,0,1,2,1,1,1,1,1,1,0,0,1,1,1,3,1,1,1,1,0,1,1,1,1,1,3,1,1,5,2,1,1,1,1,1,1,1,1,1,1,0,0,1,3,1,1,0,1,0,0,0,1,1,1,6,2,1,1,1,1,0,0,0,1,1,0,5,1,0,0,0,1,0,0,0,0,0,0,1,1,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,1,1,1,1,1,1,1,0,1,1,1,3,1,1,1,1,1,1,0,1,0,1,0,2,0,1,1,3,1,1,1,1,1,5,1,1,1,2,1,1,1,1,1,1,3,1,1,1,1,1,0,0,1,1,1,3,0,1,0,0,1,0,0,0,1,1,5,1,2,1,1,0,0,1,0,1,0,1,1,1,1,3,1,1,1,1,1,1,0,0,0,0,1,1,0,0,0,0,1,1,2,1,1,1,0,1,1,1,1,1,0,0,0,0,0,0,1,1,1,1,0,0,0,2,1,1,0,0,0,0,0,2,1,1,0,0,1,0,3,0,1,0,0,1,0,0,1,0,1,0,0,1,1,1,0,0,2,2,1,1,1,1,0,1,1,1,0,0,1,1,1,1,1,1,1,1,1,1,0,1,0,0,1,0,1,2,1,0,1,0,1,1,1,1,1,1,1,0,0,0,0,2,2,0,1,1,0,1,1,0,1,0,0,1,0,0,2,1,1,5,0,1,0,2,1,1,0,3,3,0,0,0,1,4,3,0,1,1,1,1,2,1,1,0,0,0,0,0,3,0,0,0,0,1,0,0,0,1,1,1,1,2,1,2,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,2,1,1,1,1,1,1,1,4,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,12,3,1,3,0,0,0,0,0,2,1,1,1,0,0,0,0,0,0,1,1,0,1,0,0,0,0,0,1,0,0,0,2,1,1,1,0,0,0,1,1,1,2,1,1,1,1,1,1,0,0,1,1,1,1,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,1,1,0,0,1,10,3,1,3,0,1,3,2,0,0,1,1,1,1,1,1,0,1,1,0,0,0,1,1,1,1,1,2,1,1,1,1,1,1,3,1,1,1,1,0,0,2,2,12,9,1,9,1,1,1,1,1,1,1,1,1,1,1,0,0,0,1,1,1,1,1,0,0,0,2,0,0,0,0,2,1,1,3,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,3,0,1,0,0,1,0,0,0,0,0,0,1,1,1,1,0,0,0,1,0,1,1,1,1,0,0,2,1,1,1,1,1,1,1,0,0,2,2,1,2,2,1,1,1,1,1,1,0,0,0,1,1,1,1,2,1,1,0,0,0,0,0,0,0,0,0,0,1,6,3,4,1,0,6,2,1,1,5,4,0,1,1,1,1,2,0,0,0,0,0,1,4,1,0,5,4,0,0,0,0,0,0,1,2,1,0,4,2,0,0,1,0,1,1,0,1,1,0,0,0,11,1,1,2,1,1,1,1,3,3,7,0,3,3,5,2,1,3,1,1,1,1,1,1,0,1,1,0,1,1,1,1,1,0,0,0,25,20,0,15,1,0,1,4,8,5,2,1,0,1,1,3,0,2,1,0,3,3,0,2,1,3,0,0,1,0,0,2,1,1,0,0,1,0,2,1,0,2,0,0,1,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,3,5,1,2,1,3,1,1,1,1,3,1,1,3,1,1,1,1,1,1,1,1,1,4,2,1,1,2,2,0,1,1,1,1,1,1,1,0,1,1,1,1,1,2,2,1,0,1,0,0,0,1,1,1,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,3,2,1,1,1,0,1,1,1,0,1,1,1,0,0,0,1,2,1,2,0,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,0,0,0,0,0,2,1,13,8,1,2,4,0,2,3,1,1,1,2,2,1,1,1,1,0,1,1,1,1,1,1,1,0,1,1,0,1,1,1,1,1,0,0,0,1,4,2,1,1,1,2,1,0,0,0,0,0,0,1,1,1,1,0,0,0,0,0,0,4,1,1,1,0,0,0,0,0,0,0,1,2,1,1,2,2,1,1,1,1,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,3,1,3,1,1,56,8,0,0,5,7,0,0,0,0,0,0,11,7,1,0,1,2,7,0,0,1,1,0,0,12,0,1,0,0,1,0,0,3,0,0,1,0,0,0,0,0,0,0,0,0,0,1,0,7,0,1,2,0,2,1,0,0,0,1,0,0,2,1,0,0,0,8,0,0,1,0,0,0,2,0,0,0,0,1,1,1,1,1,1,1,1,0,1,0,0,0,0,0,0,0,1,1,3,1,0,0,1,1,1,0,1,0,0,0,0,1,1,1,1,1,0,0,0,0,1,1,1,4,1,0,0,0,0,5,0,0,0,0,6,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,2,2,1,3,1,1,0,0,1,1,1,0,1,0,0,1,0,0,1,1,1,2,1,0,0,1,0,1,1,1,1,1,1,1,0,0,0,1,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,1,1,0,1,0,1,0,1,1,1,1,1,0,2,1,0,1,1,1,1,3,1,1,1,0,0,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,4,2,0,1,1,1,2,1,1,1,0,0,0,1,0,0,1,1,1,1,1,1,1,1,5,5,1,1,1,2,0,1,0,1,1,1,0,1,0,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,1,1,1,1,1,1,1,0,0,1,1,1,0,1,1,1,1,0,0,0,11,1,1,8,1,1,1,1,1,1,1,1,14,2,0,10,1,1,1,1,1,1,2,7,1,1,0,1,1,2,0,1,1,1,0,1,1,1,1,1,1,1,1,1,0,1,1,0,1,0,0,0,0,0,0,0,0,0,0,1,1,2,1,1,1,0,0,0,0,1,1,1,0,3,2,2,1,1,1,1,1,1,1,1,1,1,1,0,0,1,0,0,0,0,0,1,1,1,1,1,1,1,1,27,1,0,3,0,1,3,0,2,0,0,3,1,3,1,0,0,2,0,1,0,1,2,1,2,1,3,3,1,2,1,1,1,1,4,1,0,0,0,1,0,2,1,2,0,0,0,2,3,0,0,0,1,2,1,1,1,1,1,1,2,1,1,2,1,1,1,0,0,1,1,1,2,1,3,0,3,3,0,1,1,1,2,0,0,0,0,0,0,0,2,0,0,0,0,0,0,1,7,0,0,0,0,0,1,6,1,1,4,3,0,1,1,2,5,0,0,2,0,1,1,0,0,1,1,0,0,0,1,1,1,2,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,2,1,1,1,1,1,1,1,1,1,0,1,0,1,1,1,14,2,0,0,2,3,1,1,0,3,1,4,0,2,8,0,0,2,1,1,0,1,0,0,0,1,1,0,2,0,0,0,0,2,1,0,1,0,0,0,0,0,0,0,1,1,0,1,0,1,1,3,1,1,6,0,0,1,0,0,0,0,0,5,2,1,2,0,1,5,0,0,1,0,0,0,0,0,0,0,2,0,0,1,0,0,0,0,0,0,0,0,1,1,1,3,1,1,1,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,1,1,1,1,0,1,0,1]

answerarr = [0,0,0,0,13,5,1,1,3,0,1,1,1,2,0,0,1,1,1,1,26,8,3,2,8,4,1,1,1,5,6,2,2,1,1,1,1,1,4,1,1,1,1,1,1,1,1,1,2,1,1,1,0,1,1,1,1,1,1,0,1,1,1,0,0,0,1,1,1,0,0,0,0,0,0,2,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,1,0,0,1,0,0,0,0,0,0,0,1,1,0,0,0,1,1,1,1,0,0,1,0,1,0,0,0,1,0,1,1,0,1,0,0,0,0,11,1,2,2,1,1,0,0,1,1,3,1,1,1,1,0,0,0,1,1,0,0,1,1,1,0,0,1,1,0,2,0,0,2,0,1,0,0,0,0,2,1,1,1,1,1,6,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,1,1,0,0,0,1,0,0,0,0,0,0,0,2,1,1,1,1,0,0,1,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,1,0,0,0,0,0,62,3,2,7,6,17,1,2,1,1,3,3,2,3,1,7,6,2,3,2,0,1,1,1,1,2,0,0,1,1,2,1,3,1,2,1,2,1,1,2,1,2,1,1,1,1,0,0,0,3,1,1,4,1,1,0,1,0,0,0,0,1,1,0,0,5,1,0,1,0,1,0,2,1,1,0,1,0,0,39,3,1,1,2,2,1,1,5,5,2,1,9,1,1,3,2,1,3,1,1,3,2,0,8,1,1,1,1,1,2,2,0,1,2,1,2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,4,1,1,0,0,0,0,0,0,0,1,1,1,2,1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,0,1,0,1,1,1,1,0,0,0,0,0,0,0,0,1,0,0,0,0,1,0,0,0,1,1,1,1,6,2,1,2,0,1,0,0,2,1,1,9,3,1,1,3,4,1,1,0,1,1,1,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,21,1,20,1,0,0,0,0,0,0,0,0,1,0,0,1,1,1,1,2,0,0,1,0,0,0,0,1,0,1,1,0,0,0,0,0,0,1,1,1,1,0,2,1,1,1,1,0,0,0,0,0,0,0,0,1,1,0,0,0,3,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,1,0,1,1,1,0,0,0,13,0,0,0,2,0,1,4,1,0,2,1,11,4,1,1,1,0,2,1,1,1,2,1,0,0,1,1,1,1,1,1,0,0,0,3,3,3,1,1,1,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,1,0,1,0,2,0,1,0,0,0,0,0,0,0,0,1,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,3,1,0,1,1,0,1,2,2,0,0,2,0,1,0,1,1,1,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,0,0,1,1,1,1,1,0,0,0,0,0,1,0,0,0,0,0,4,4,1,1,1,1,0,0,0,0,1,1,1,0,0,0,1,1,1,1,1,0,0,0,1,1,0,1,16,2,0,1,4,0,1,1,0,5,0,1,2,0,0,0,2,1,0,0,0,0,2,1,1,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,1,6,3,1,0,1,6,0,0,1,0,1,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,0,1,1,0,1,1,0,2,2,0,0,0,35,5,1,1,0,6,1,1,1,3,1,1,1,10,9,0,1,0,0,0,0,2,1,1,2,2,1,1,2,0,1,1,1,1,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,37,3,4,9,1,2,1,1,4,0,0,0,3,1,1,2,1,1,1,0,4,1,1,1,1,1,1,1,3,1,1,2,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,1,1,0,1,1,0,6,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,1,1,0,0,2,2,0,13,1,1,2,1,4,2,3,1,1,0,0,1,0,0,1,3,0,0,1,2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,1,1,0,1,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,40,4,1,5,10,1,1,2,8,2,1,5,0,1,1,1,2,2,1,1,1,1,5,1,1,2,3,1,1,1,3,1,2,1,1,3,1,0,2,2,1,1,1,3,1,1,1,0,0,0,0,1,1,1,0,2,0,2,0,0,1,1,0,0,0,0,0,0,0,0,1,1,34,0,0,0,34,0,0,0,0,0,0,1,1,1,0,0,0,0,1,0,0,1,1,1,1,1,1,1,2,1,1,0,6,1,2,0,1,3,0,0,0,0,1,1,0,0,0,1,1,1,1,1,1,1,0,0,0,1,7,2,1,1,1,1,1,1,0,0,0,1,6,5,1,3,0,1,0,4,2,0,0,1,1,1,0,0,0,0,0,0,0,0,1,0,5,1,0,0,1,1,0,0,0,1,0,0,0,0,1,1,0,1,0,0,0,0,0,1,1,1,59,14,4,47,7,1,5,17,10,4,1,0,2,12,0,4,1,0,0,1,5,9,1,2,0,5,2,1,2,2,2,6,2,2,1,1,1,1,5,2,5,4,1,2,4,1,1,1,2,3,2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,3,0,0,1,1,1,1,1,0,0,0,1,0,0,0,1,5,2,1,1,1,1,1,1,1,1,1,0,0,0,0,0,2,0,0,1,1,0,0,0,1,1,1,1,0,0,0,1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,2,1,1,1,1,0,0,3,0,0,0,0,1,0,0,0,0,1,0,1,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,1,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,1,3,1,2,1,1,0,0,0,0,1,2,1,1,1,1,0,0,0,0,2,1,1,1,1,1,1,0,0,0,0,1,1,0,0,0,0,1,1,1,1,1,1,3,3,0,0,0,0,0,0,0,0,0,0,0,0,211,34,1,1,19,70,4,1,10,1,1,18,25,10,11,1,0,10,34,1,3,0,11,2,1,12,2,2,1,1,1,1,1,18,2,1,11,1,2,1,5,2,1,3,5,1,1,1,2,14,1,1,4,1,0,2,5,1,6,6,4,2,0,5,9,2,2,13,1,2,3,1,1,5,4,2,1,1,1,0,0,0,0,0,0,0,0,1,0,1,3,2,1,1,1,1,0,0,9,0,1,4,0,0,0,1,0,1,1,1,1,0,0,0,0,0,2,1,1,1,0,0,0,0,0,1,1,1,1,6,1,34,36,5,37,1,1,1,4,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,0,1,0,1,1,3,1,1,0,0,0,0,0,1,1,0,1,0,0,0,0,0,0,0,1,1,1,0,1,1,1,1,2,1,1,1,1,0,0,0,1,1,1,0,0,1,0,1,0,1,0,0,0,0,0,1,0,0,1,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,1,1,0,0,1,1,1,0,0,1,0,1,0,0,0,1,0,1,1,3,1,1,1,1,1,1,0,0,0,0,0,0,0,3,0,0,0,0,0,1,1,1,0,0,0,1,0,1,0,0,1,0,1,0,1,1,1,1,0,0,0,1,1,0,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,1,1,0,0,0,1,0,0,0,0,1,1,1,2,0,0,1,0,0,0,0,0,0,0,0,8,1,1,2,0,1,1,1,2,0,0,3,0,1,1,0,0,1,1,0,0,1,2,0,0,0,0,0,0,0,0,0,1,1,1,1,3,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,1,1,1,2,0,0,1,2,0,0,0,0,0,0,0,0,0,0,0,1,0,0,1,1,0,1,1,1,1,1,0,0,0,0,0,0,0,0,14,1,2,3,1,2,1,2,3,1,1,3,0,1,1,1,1,0,1,0,1,1,0,1,0,0,0,0,1,0,0,0,0,0,26,12,1,3,1,2,1,1,1,0,2,1,1,0,1,3,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,5,1,2,0,1,0,0,2,0,1,2,1,3,3,1,1,0,1,3,3,1,1,1,0,6,1,1,1,1,1,0,6,0,0,5,1,1,0,0,0,0,1,1,0,1,2,0,1,1,0,0,1,1,1,0,0,0,98,6,13,34,5,5,2,7,1,1,2,10,1,1,2,3,2,1,1,1,15,1,5,9,7,2,1,1,7,1,1,3,1,6,5,2,1,1,6,1,1,1,2,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,1,0,0,82,9,1,1,6,19,1,7,6,6,3,5,2,3,11,1,3,4,0,3,1,1,10,3,1,1,1,1,1,3,1,2,3,2,1,1,0,1,1,2,1,1,4,2,0,0,1,2,1,0,0,0,0,0,48,2,5,12,3,1,3,1,5,2,2,2,5,5,2,0,1,2,1,1,2,4,1,2,5,3,0,1,1,3,5,1,2,1,1,1,1,1,0,0,0,0,0,0,0,3,1,1,1,1,0,0,0,2,1,4,2,2,1,2,2,1,1,0,0,0,0,1,0,1,0]


objectarr = [0,0,0,0,13,5,1,1,3,0,1,1,1,2,0,0,1,1,1,1,26,8,3,2,8,4,1,1,1,5,6,2,2,1,1,1,1,1,4,1,1,1,1,1,1,1,1,1,2,1,1,1,0,1,1,1,1,1,1,0,1,1,1,0,0,0,1,1,1,0,0,0,0,0,0,2,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,1,0,0,1,0,0,0,0,0,0,0,1,1,0,0,0,1,1,1,1,0,0,1,0,1,0,0,0,1,0,1,1,0,1,0,0,0,0,11,1,2,2,1,1,0,0,1,1,3,1,1,1,1,0,0,0,1,1,0,0,1,1,1,0,0,1,1,0,2,0,0,2,0,1,0,0,0,0,2,1,1,1,1,1,6,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,1,1,0,0,0,1,0,0,0,0,0,0,0,2,1,1,1,1,0,0,1,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,1,0,0,0,0,0,62,3,2,7,6,17,1,2,1,1,3,3,2,3,1,7,6,2,3,2,0,1,1,1,1,2,0,0,1,1,2,1,3,1,2,1,2,1,1,2,1,2,1,1,1,1,0,0,0,3,1,1,4,1,1,0,1,0,0,0,0,1,1,0,0,5,1,0,1,0,1,0,2,1,1,0,1,0,0,39,3,1,1,2,2,1,1,5,5,2,1,9,1,1,3,2,1,3,1,1,3,2,0,8,1,1,1,1,1,2,2,0,1,2,1,2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,4,1,1,0,0,0,0,0,0,0,1,1,1,2,1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,0,1,0,1,1,1,1,0,0,0,0,0,0,0,0,1,0,0,0,0,1,0,0,0,1,1,1,1,6,2,1,2,0,1,0,0,2,1,1,9,3,1,1,3,4,1,1,0,1,1,1,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,21,1,20,1,0,0,0,0,0,0,0,0,1,0,0,1,1,1,1,2,0,0,1,0,0,0,0,1,0,1,1,0,0,0,0,0,0,1,1,1,1,0,2,1,1,1,1,0,0,0,0,0,0,0,0,1,1,0,0,0,3,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,1,0,1,1,1,0,0,0,13,0,0,0,2,0,1,4,1,0,2,1,11,4,1,1,1,0,2,1,1,1,2,1,0,0,1,1,1,1,1,1,0,0,0,3,3,3,1,1,1,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,1,0,1,0,2,0,1,0,0,0,0,0,0,0,0,1,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,3,1,0,1,1,0,1,2,2,0,0,2,0,1,0,1,1,1,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,0,0,1,1,1,1,1,0,0,0,0,0,1,0,0,0,0,0,4,4,1,1,1,1,0,0,0,0,1,1,1,0,0,0,1,1,1,1,1,0,0,0,1,1,0,1,16,2,0,1,4,0,1,1,0,5,0,1,2,0,0,0,2,1,0,0,0,0,2,1,1,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,1,6,3,1,0,1,6,0,0,1,0,1,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,0,1,1,0,1,1,0,2,2,0,0,0,35,5,1,1,0,6,1,1,1,3,1,1,1,10,9,0,1,0,0,0,0,2,1,1,2,2,1,1,2,0,1,1,1,1,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,37,3,4,9,1,2,1,1,4,0,0,0,3,1,1,2,1,1,1,0,4,1,1,1,1,1,1,1,3,1,1,2,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,1,1,0,1,1,0,6,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,1,1,0,0,2,2,0,13,1,1,2,1,4,2,3,1,1,0,0,1,0,0,1,3,0,0,1,2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,1,1,0,1,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,40,4,1,5,10,1,1,2,8,2,1,5,0,1,1,1,2,2,1,1,1,1,5,1,1,2,3,1,1,1,3,1,2,1,1,3,1,0,2,2,1,1,1,3,1,1,1,0,0,0,0,1,1,1,0,2,0,2,0,0,1,1,0,0,0,0,0,0,0,0,1,1,34,0,0,0,34,0,0,0,0,0,0,1,1,1,0,0,0,0,1,0,0,1,1,1,1,1,1,1,2,1,1,0,6,1,2,0,1,3,0,0,0,0,1,1,0,0,0,1,1,1,1,1,1,1,0,0,0,1,7,2,1,1,1,1,1,1,0,0,0,1,6,5,1,3,0,1,0,4,2,0,0,1,1,1,0,0,0,0,0,0,0,0,1,0,5,1,0,0,1,1,0,0,0,1,0,0,0,0,1,1,0,1,0,0,0,0,0,1,1,1,59,14,4,47,7,1,5,17,10,4,1,0,2,12,0,4,1,0,0,1,5,9,1,2,0,5,2,1,2,2,2,6,2,2,1,1,1,1,5,2,5,4,1,2,4,1,1,1,2,3,2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,3,0,0,1,1,1,1,1,0,0,0,1,0,0,0,1,5,2,1,1,1,1,1,1,1,1,1,0,0,0,0,0,2,0,0,1,1,0,0,0,1,1,1,1,0,0,0,1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,2,1,1,1,1,0,0,3,0,0,0,0,1,0,0,0,0,1,0,1,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,1,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,1,3,1,2,1,1,0,0,0,0,1,2,1,1,1,1,0,0,0,0,2,1,1,1,1,1,1,0,0,0,0,1,1,0,0,0,0,1,1,1,1,1,1,3,3,0,0,0,0,0,0,0,0,0,0,0,0,211,34,1,1,19,70,4,1,10,1,1,18,25,10,11,1,0,10,34,1,3,0,11,2,1,12,2,2,1,1,1,1,1,18,2,1,11,1,2,1,5,2,1,3,5,1,1,1,2,14,1,1,4,1,0,2,5,1,6,6,4,2,0,5,9,2,2,13,1,2,3,1,1,5,4,2,1,1,1,0,0,0,0,0,0,0,0,1,0,1,3,2,1,1,1,1,0,0,9,0,1,4,0,0,0,1,0,1,1,1,1,0,0,0,0,0,2,1,1,1,0,0,0,0,0,1,1,1,1,6,1,34,36,5,37,1,1,1,4,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,0,1,0,1,1,3,1,1,0,0,0,0,0,1,1,0,1,0,0,0,0,0,0,0,1,1,1,0,1,1,1,1,2,1,1,1,1,0,0,0,1,1,1,0,0,1,0,1,0,1,0,0,0,0,0,1,0,0,1,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,1,1,0,0,1,1,1,0,0,1,0,1,0,0,0,1,0,1,1,3,1,1,1,1,1,1,0,0,0,0,0,0,0,3,0,0,0,0,0,1,1,1,0,0,0,1,0,1,0,0,1,0,1,0,1,1,1,1,0,0,0,1,1,0,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,1,1,0,0,0,1,0,0,0,0,1,1,1,2,0,0,1,0,0,0,0,0,0,0,0,8,1,1,2,0,1,1,1,2,0,0,3,0,1,1,0,0,1,1,0,0,1,2,0,0,0,0,0,0,0,0,0,1,1,1,1,3,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,1,1,1,2,0,0,1,2,0,0,0,0,0,0,0,0,0,0,0,1,0,0,1,1,0,1,1,1,1,1,0,0,0,0,0,0,0,0,14,1,2,3,1,2,1,2,3,1,1,3,0,1,1,1,1,0,1,0,1,1,0,1,0,0,0,0,1,0,0,0,0,0,26,12,1,3,1,2,1,1,1,0,2,1,1,0,1,3,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,5,1,2,0,1,0,0,2,0,1,2,1,3,3,1,1,0,1,3,3,1,1,1,0,6,1,1,1,1,1,0,6,0,0,5,1,1,0,0,0,0,1,1,0,1,2,0,1,1,0,0,1,1,1,0,0,0,98,6,13,34,5,5,2,7,1,1,2,10,1,1,2,3,2,1,1,1,15,1,5,9,7,2,1,1,7,1,1,3,1,6,5,2,1,1,6,1,1,1,2,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,1,0,0,82,9,1,1,6,19,1,7,6,6,3,5,2,3,11,1,3,4,0,3,1,1,10,3,1,1,1,1,1,3,1,2,3,2,1,1,0,1,1,2,1,1,4,2,0,0,1,2,1,0,0,0,0,0,48,2,5,12,3,1,3,1,5,2,2,2,5,5,2,0,1,2,1,1,2,4,1,2,5,3,0,1,1,3,5,1,2,1,1,1,1,1,0,0,0,0,0,0,0,3,1,1,1,1,0,0,0,2,1,4,2,2,1,2,2,1,1,0,0,0,0,1,0,1,0]


'''x = np.random.normal(size = 1000)
plt.hist(questionarr, normed=True, bins=150)
plt.ylabel('Probability');
plt.show()'''



 
#objects = ('Python', 'C++', 'Java', 'Perl', 'Scala', 'Lisp')
'''objects = objectarr
y_pos = np.arange(len(objects))
performance = questionarr
 
plt.bar(y_pos, performance, align='center', alpha=0.5)
plt.xticks(y_pos, objects)
plt.ylabel('Usage')
plt.title('Programming language usage')
 
plt.show()'''

'''r = redis.Redis('localhost')
read_dict = r.hget('test', 'orgact')
read_dict = json.loads(read_dict)
print read_dict'''

def plot_hist(objects, performance):
	#objects = user_id
	y_pos = np.arange(len(objects))
	#performance = user_activity
	 
	'''plt.bar(y_pos, performance, align='center', alpha=0.5)
	plt.xticks(y_pos, objects)
	plt.ylabel('Usage')
	plt.title('Programming language usage')
	plt.show()'''
	#a = np.hstack((user_activity.normal(size=1000),user_activity.normal(loc=5, scale=2, size=1000)))
	plt.hist(performance, bins='auto')  # arguments are passed to np.histogram
	#plt.hist(performance, bins=[0,1,2,3,4,5,6,7,8,9,10])
	plt.title("Histogram with 'auto' bins")
	plt.show()

def get_user_answer_stats(cnx):
	query = "SELECT OwnerUserId, COUNT(*) FROM Posts where OwnerUserId is not null and PostTypeId = 2 GROUP BY OwnerUserId;"
	print 'query -->', query
	cursor = cnx.cursor()
	try:
		user_activity = []
		user_id = []
		cursor.execute(query);
		data = cursor.fetchall();
		for row in data:
			user_id.append(row[0])
			#print row[1]
			user_activity.append(row[1])
	    #sys.exit();
		user_activity_stats = stats.describe(user_activity)
		print 'user answer activity stats-->', user_activity_stats
		plot_hist(user_id, user_activity)

	except Exception as e:
	    print ("selection query!!!");
	    print(e)
	    sys.exit();

def get_user_question_stats(cnx):
	query = "SELECT OwnerUserId, COUNT(*) FROM Posts where OwnerUserId is not null and PostTypeId = 1 GROUP BY OwnerUserId;"
	print 'query -->', query
	cursor = cnx.cursor()
	try:
		user_activity = []
		user_id = []
		cursor.execute(query);
		data = cursor.fetchall();
		for row in data:
			user_id.append(row[0])
			#print row[1]
			user_activity.append(row[1])
	    #sys.exit();
		user_activity_stats = stats.describe(user_activity)
		print 'user question activity stats-->', user_activity_stats
		plot_hist(user_id, user_activity)

	except Exception as e:
	    print ("selection query!!!");
	    print(e)
	    sys.exit();


def get_stats_from_db(cnx):
	query = "SELECT OwnerUserId, COUNT(*) FROM Posts where OwnerUserId is not null GROUP BY OwnerUserId;"
	print 'query -->', query
	cursor = cnx.cursor()
	try:
		user_activity = []
		user_id = []
		cursor.execute(query);
		data = cursor.fetchall();
		for row in data:
			user_id.append(row[0])
			#print row[1]
			user_activity.append(row[1])
	    #sys.exit();
		user_activity_stats = stats.describe(user_activity)
		print 'user activity stats-->', user_activity_stats
		#user_activity_mean = np.mean(user_activity)
		#objects = ('Python', 'C++', 'Java', 'Perl', 'Scala', 'Lisp')
		
	except Exception as e:
	    print ("selection query!!!");
	    print(e)
	    sys.exit();

def main():

	cnx = getConn();
	print cnx;
	print 'Hello World';
	#get_user_answer_stats(cnx);
	get_user_question_stats(cnx)
	#get_stats_from_db(cnx);

def getConn():
     try:
        cnx = mysql.connector.connect(user='root', password='piyush0791',
                                      host='127.0.0.1',
                                      database='forum_db')
        #print cnx
        #cnx.set_converter_class(NumpyMySQLConverter)
        
        print 'connected!!'
        return cnx
     except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Invalid user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)

        return None

if __name__ == "__main__":
	main();
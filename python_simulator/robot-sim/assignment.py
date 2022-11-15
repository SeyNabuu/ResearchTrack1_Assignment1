""" Import required libraries"""

from __future__ import print_function

import time
from sr.robot import *



""" Initializing Arrays of None and length 6, and variables,a and b for incrementing the arrays """

a=0
b=0
liste_silver_token=[None] * 6
liste_golden_token=[None] * 6



""" float: Threshold for the control of the linear distance for both Tokens (SILVER/GOLD)"""


a_th = 2.0  # float: Threshold for the control of the orientation

d_th = 0.4   # float: Threshold for the control of the linear distance for silver token
 
d_th1 = 0.5  # float: Threshold for the control of the linear distance for golden token 
 


""" instance of the class Robot"""
 
R = Robot()



 
def drive(speed, seconds):
    """
    Function for setting a linear velocity
    
    Args: speed (int): the speed of the wheels
	  seconds (int): the time interval
    """
    R.motors[0].m0.power = speed 
    R.motors[0].m1.power = speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

def turn(speed, seconds):
    """
    Function for setting an angular velocity
    
    Args: speed (int): the speed of the wheels
	  seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = -speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

def find_silver_token():
    """
    Function to find the closest silver token
    Returns:
	dist (float): distance of the closest silver token (-1 if no silver token is detected)
	rot_y (float): angle between the robot and the silver token (-1 if no silver token is detected)
	Silver_Token_number(integer):offset of the numeric code of the marker from the lowest numbered marker of its type.This will give us an unique number associated with each silver Token
	
	
    """
    
    
    dist=100
    for token in R.see():
        if token.dist < dist and token.info.marker_type is MARKER_TOKEN_SILVER:
            dist=token.dist
	    rot_y=token.rot_y
	    Silver_Token_number=token.info.offset 
    if dist==100:
	return -1, -1, -1
    else:
   	return Silver_Token_number,dist, rot_y
   	

def find_golden_token():
    """
    Function to find the closest golden token
    Returns:
	dist (float): distance of the closest golden token (-1 if no golden token is detected)
	rot_y (float): angle between the robot and the golden token (-1 if no golden token is detected)
	Golden_Token_number(integer):offset of the numeric code of the marker from the lowest numbered marker of its type.This will give us the unique number associated with each Golden Token
	
    """
    
    
    dist=100
    for token in R.see():
        if token.dist < dist and token.info.marker_type is MARKER_TOKEN_GOLD:
            dist=token.dist
	    rot_y=token.rot_y
	    Golden_Token_number=token.info.offset 
    if dist==100:
	return -1, -1, -1
    else:
   	return Golden_Token_number,dist, rot_y
   	
   
   	
def Match_silver_with_golden():

    """
    Function to put the Silver Token close to the Golden Token
    The Robot will try to find the closest Golden token by checking the distance from Golden token.
    When distance is lesser than set threshold then the Robot releases the Silver token which was already grabbed. 
    We break the loop if the silver Token is released Then the code goes back to the main loop """


    global b   # this will allows us to use the variable b inside the fonction
    while 1:  
    	""" 
    Check if the golden token is in our List. 
    	 Thus,Robot will only match the Silver token with the Golden token whose number is not previously stored in our list.then, we add the number of the golden token in our list and increase the value of the index
    	 
	"""
    	Golden_Token_number,dist1, rot_y1, = find_golden_token()
    	 
    	if Golden_Token_number not in liste_golden_token:
    	
            
		if dist1==-1:
	       		print("I don't see any  Golden token!!")
			turn(+10,1)
	   	elif dist1 <=d_th1: 
			print("Golden token ",Golden_Token_number,"was found")
			R.release() # if Golden token is enough near,we release the Silver token.
			turn(+20, 1.5)
			print("Silver token ",Silver_Token_number,"was succesfully putted close to  Golden token",Golden_Token_number)
			liste_golden_token[b]=Golden_Token_number  
			b=b+1    
			break   #Break the while loop
		elif -a_th<= rot_y1 <= a_th: 	
	       		print("Ah, here we are")
	       		drive(30, 1.5)
	    	elif rot_y1 < -a_th:
	      		print("Left a bit...")
	       		turn(-2, 0.5)
	    	elif rot_y1 > a_th:
	       		print("Right a bit...")
	       		turn(+2, 0.5)



"""Main While loop of the Code: """



while 1:
    
	Silver_Token_number,dist, rot_y, = find_silver_token()
	
    	if Silver_Token_number not in liste_silver_token: 
    	
    		""" Check if the Silver token is in our List. Thus,Robot will only match the golden Token with the silver token whose number is not previously stored in our List 
    		"""
		if dist==-1: 
			print("I don't see any Silver token!!")
			turn(+30, 1.5)
		elif dist <d_th:
			print("Silver token ",Silver_Token_number,"was found")
			if R.grab():
			
				""" if the Silver token is grabbed,we call the fonction  Match_with_golden.Thus,Robot will match the grabbed Silver Token with a golden token whose number is not in our list.then, we add the number of the silver token in our list and increase the value of the index.
				"""
			
				liste_silver_token[a]=Silver_Token_number 
				a=a+1  
				print("silver token",Silver_Token_number,"was grabbed succesfully.")
				turn(+20,1.5)
			    	Match_silver_with_golden()
			    	turn(-20,0.5)
			    	 
			      
			else:
				print("Aww, I'm not close enough.")
		elif -a_th<= rot_y <= a_th:
			print("Ah, that'll do.")
			drive(30, 1)
		elif rot_y < -a_th:
			print("Left a bit...")
			turn(-2, 0.5)
		elif rot_y > a_th:
		 	print("Right a bit...")
			turn(+2, 0.5)
	if None not in liste_golden_token and None not in liste_silver_token:  # Check if all the 6 tokens are paired properly .
	
		print("List of golden token numbers: ",liste_golden_token)
		print("List of Silver token numbers: ",liste_silver_token)
		print("Mission Accomplished")
		exit ()	



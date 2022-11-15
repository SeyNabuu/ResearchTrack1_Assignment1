Python Robotics Simulator : ASSIGNMENT
================================

This is a simple, portable robot simulator developed by [Student Robotics](https://studentrobotics.org).
Some of the arenas have been modified for the Research Track I course.

In the following lines,we will have at first a brief explanation of the environnement ,the robot,its attributes and its functioning.Then we will develop the assignment.

To see other exemples of how the robot works,you can click on this link (https://github.com/CarmineD8/python_simulator).
You will have some exercises with their solutions.

Installing and running
----------------------

The simulator requires a Python 2.7 installation, the [pygame](http://pygame.org/) library, [PyPyBox2D](https://pypi.python.org/pypi/pypybox2d/2.1-r331), and [PyYAML](https://pypi.python.org/pypi/PyYAML/).

Pygame, unfortunately, can be tricky (though [not impossible](http://askubuntu.com/q/312767)) to install in virtual environments. If you are using `pip`, you might try `pip install hg+https://bitbucket.org/pygame/pygame`, or you could use your operating system's package manager. Windows users could use [Portable Python](http://portablepython.com/). PyPyBox2D and PyYAML are more forgiving, and should install just fine using `pip` or `easy_install`.

## Troubleshooting

When running `python run.py <file>`, you may be presented with an error: `ImportError: No module named 'robot'`. This may be due to a conflict between sr.tools and sr.robot. To resolve, symlink simulator/sr/robot to the location of sr.tools.

On Ubuntu, this can be accomplished by:
* Find the location of srtools: `pip show sr.tools`
* Get the location. In my case this was `/usr/local/lib/python2.7/dist-packages`
* Create symlink: `ln -s path/to/simulator/sr/robot /usr/local/lib/python2.7/dist-packages/sr/`

Robot API
---------

The API for controlling a simulated robot is designed to be as similar as possible to the [SR API][sr-api].


### Motors ###

The simulated robot has two motors configured for skid steering, connected to a two-output [Motor Board](https://studentrobotics.org/docs/kit/motor_board). The left motor is connected to output `0` and the right motor to output `1`.

The Motor Board API is identical to [that of the SR API](https://studentrobotics.org/docs/programming/sr/motors/), except that motor boards cannot be addressed by serial number. So, to turn on the spot at one quarter of full power, one might write the following:

```python
R.motors[0].m0.power = 25
R.motors[0].m1.power = -25
```

### Vision ###

To help the robot find tokens and navigate, each token has markers stuck to it, as does each wall. The `R.see` method returns a list of all the markers the robot can see, as `Marker` objects. The robot can only see markers which it is facing towards.

Each `Marker` object has the following attributes:

* `info`: a `MarkerInfo` object describing the marker itself. Has the following attributes:
  * `code`: the numeric code of the marker.
  * `marker_type`: the type of object the marker is attached to (either `MARKER_TOKEN_GOLD`, `MARKER_TOKEN_SILVER` or `MARKER_ARENA`).
  * `offset`: offset of the numeric code of the marker from the lowest numbered marker of its type. For example, token number 3 has the code 43, but offset 3.
  * `size`: the size that the marker would be in the real game, for compatibility with the SR API.
* `centre`: the location of the marker in polar coordinates, as a `PolarCoord` object. Has the following attributes:
  * `length`: the distance from the centre of the robot to the object (in metres).
  * `rot_y`: rotation about the Y axis in degrees.
* `dist`: an alias for `centre.length`
* `res`: the value of the `res` parameter of `R.see`, for compatibility with the SR API.
* `rot_y`: an alias for `centre.rot_y`
* `timestamp`: the time at which the marker was seen (when `R.see` was called).


## ASSIGNMENT 
-----------------------------
### Instruction ### 

Write a python code that:
- search and find a silver box in the environment
- put this silver box close to a golden box

In the end you should try to have silver and golden boxes distributed in pairs.


### Used Functions ###

* `R.see`: returns a list of all the markers the robot can see, as `Marker` objects. The robot can only see markers which it is facing towards.

* `R.grab()` : this function returns `True` if a token was successfully picked up, or `False` otherwise. The robot is equipped with a grabber, capable of picking up a token which is in front of the robot and within 0.4 metres of the robot's centre.
If the robot is already holding a token, it will throw an `AlreadyHoldingSomethingException`.

* `R.release()` : We call this fonction to drop the token.

* `turn()` :  Function for setting an angular velocity.
  * The speed (int): the speed of the wheels.
  * The seconds (int): the time interval.
   
* `drive()` : Function for setting a linear velocity.The arguments are :
  * The speed (int): the speed of the wheels.
  * The seconds (int): the time interval.

* `find_silver_token()` : Function to find the closest silver token.It returns:
  * `dist(float)`: distance of the closest silver token (-1 if no silver token is detected).
  * `rot_y (float)`: angle between the robot and the silver token (-1 if no silver token is detected).
  * `Silver_Token_number(int)` : Offset of the numeric code of the marker from the lowest numbered marker of its type.This will give us an unique number associated with each silver token.
	   
* `find_golden_token()` : Function to find the closest golden token.It returns:
  * `dist1(float)`: distance of the closest golden token (-1 if no golden token is detected)
  * `rot_y1 (float)`: angle between the robot and the golden token (-1 if no golden token is detected).
  * `Golden_Token_number(int)` : Offset of the numeric code of the marker from the lowest numbered marker of its type.This will give us an unique number associated with each silver Token.
	
* `Match_silver_with_golden()` : Function to put the silver token close to the golden token.
    We make the variable b global so that we can use it inside the function.
   
    At first,we check if the golden token is in our List `Liste_Golden_token`. Thus,Robot will only match the silver token with the golden token whose number is not previously stored in our list.
    The Robot will try to find the closest golden token by calling the function `find_golden_token` and checking the distance from golden token.When distance is lesser than set threshold,the Robot releases the silver token which was already grabbed using `R.release()`.We can add the number of the golden token in our list and increase the value of the index .
     
    We break the loop if the silver token is released,Then the code goes back to the main loop.

### Arrays and Varriables ###

* `Arrays` : Initializing Arrays of None and length six.We will place each matched token in these lists and then the robot will not grab them again.
  * liste_silver_token=[None] * 6
  * liste_golden_token=[None] * 6

* `Variables` :
  * a & b : Initializing variables for incrementing the arrays
  * a_th = 2.0  : Threshold for the control of the orientation
  * d_th = 0.4  : Threshold for the control of the linear distance for silver token
  * d_th1 = 0.5 : Threshold for the control of the linear distance for golden token 


### The Main Code ###

 Our main code is structured exactly like our function `Match_with_golden`.
 But here,before anything we need to find a silver token and grab it ,which we won't do in the function.
  
 At first we check if the silver token is in our List. Thus,Robot will only match the golden token with the silver token whose number is not previously stored in our List.
 The Robot will try to find the closest silver token and grab it by calling the functions `find_silver_token` and `R.grab()`.
     	If the silver token is grabbed,we call the fonction `Match_with_golden`. The Robot will  find the closest golden token and when distance is lesser than set threshold,the Robot releases the silver token.
     	We can add the number of the silver token in our list and increase the value of the index .
     	

To run the scripts in the simulator, use `run.py`, passing it the file name. 
When done, you can run the program with:

```bash
$ python run.py assignment.py
```


### Pseudocode ###

```
while True 
	call find_silver_token
	when the silver token was already not grabbed 
	
		if the silver token is not close enough
			turn to get closer
			drive to get closer

		else if the silver token is near
	   	  	print "Silver token was found"
			grab the silver token
			Add the number of the silver token in our list
            		Increase the index

			if the robot grabs the silver token
				call Find_Golden_token
				When the golden token was not already in our list 
					Call Match_with_golden token 
		        		print"Silver token was successfully putted close to  Golden token"
     	          			Add the number of the golden token in our list
                 			Increase the index
                 			Break the while 
 					
		else   
			print "I don't see any silver token!!"
	        	turn to see the whole area

	else  all the six silver token  and all the six Golden token are in their list
		print "Mission Accomplished"
		exit the code	

```
[sr-api]: https://studentrobotics.org/docs/programming/sr/

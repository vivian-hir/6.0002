# -*- coding: utf-8 -*-
# 6.100B Spring 2023
# Problem Set 3: Robot Simulation
# Name: Vivian H. 
# Collaborators: None 

import math
import random
import matplotlib

from ps3_visualize import *
import pylab

# === Provided class Position, do NOT change
class Position(object):
    """
    A Position represents a location in a two-dimensional room, where
    coordinates are given by floats (x, y).
    """
    def __init__(self, x, y):
        """
        Initializes a position with coordinates (x, y).
        """
        self.x = x
        self.y = y

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_new_position(self, angle, speed):
        """
        Computes and returns the new Position after a single clock-tick has
        passed, with this object as the current position, and with the
        specified angle and speed.

        Does NOT test whether the returned position fits inside the room.

        angle: float representing angle in degrees, 0 <= angle < 360
        speed: positive float representing speed

        Returns: a Position object representing the new position.
        """
        old_x, old_y = self.get_x(), self.get_y()

        # Compute the change in position
        delta_y = speed * math.cos(math.radians(angle))
        delta_x = speed * math.sin(math.radians(angle))

        # Add that to the existing position
        new_x = old_x + delta_x
        new_y = old_y + delta_y

        return Position(new_x, new_y)

    def __str__(self):
        return "Position: " + str(math.floor(self.x)) + ", " + str(math.floor(self.y))

# === Problem 1
class Room(object):
    """
    A Room represents a rectangular region containing clean or dusty
    tiles.

    A room has a width and a height and contains (width * height) tiles. Each tile
    has some fixed amount of dust. The tile is considered clean only when the amount
    of dust on this tile is 0.
    """
    def __init__(self, width, height, dust_amount):
        """
        Initializes a rectangular room with the specified width, height, and
        dust_amount on each tile.

        width: an integer > 0
        height: an integer > 0
        dust_amount: an integer >= 0
        """
        self.width=width
        self.height=height
        self.dust_amount=dust_amount
        self.dust_dict={}
        for w in range(width): 
            for h in range(height): 
                self.dust_dict[(w, h)]=dust_amount
        #use dictionary so position mapped to dust_amount 

    def get_dust_amount(self, w, h):
        """
        Return the amount of dust on the tile (w, h)

        Assumes that (w, h) represents a valid tile inside the room.

        w: an integer
        h: an integer

        Returns: a float
        """
        return self.dust_dict[(w,h)]
        
       

    def clean_tile_at_position(self, pos, cleaning_volume):
        """
        Mark the tile under the position pos as cleaned by cleaning_volume amount of dust.

        Assumes that pos represents a valid position inside this room.

        pos: a Position object
        cleaning_volume: a float, the amount of dust to be cleaned in a single time-step.
                  Can be negative which would mean adding dust to the tile.

        Note: The amount of dust on each tile should be NON-NEGATIVE.
              If the cleaning_volume exceeds the amount of dust on the tile, mark it as 0.
        """
        w=math.floor(pos.get_x())
        h=math.floor(pos.get_y())
        current_dust=self.get_dust_amount(w,h)
        if cleaning_volume>current_dust: #don't want a negative value 
            final_dust=0 
        else:
            final_dust=current_dust-cleaning_volume 
        self.dust_dict[(w,h)]=final_dust
        
    def is_tile_cleaned(self, w, h):
        """
        Return True if the tile (w, h) has been cleaned.

        Assumes that (w, h) represents a valid tile inside the room.

        w: an integer
        h: an integer

        Returns: True if the tile (w, h) is cleaned, False otherwise

        Note: The tile is considered clean only when the amount of dust on this
              tile is 0.
        """
        if self.get_dust_amount(w,h)==0:
            return True 
        else:
            return False 
        
    def get_num_cleaned_tiles(self):
        """
        Returns: an integer; the total number of clean tiles in the room
        """
        counter=0
        for h in range(self.height):
            for w in range(self.width): 
                if self.get_dust_amount(w,h)==0:
                    counter+=1
        return counter 

    def is_position_in_room(self, pos):
        """
        Determines if pos is inside the room.

        pos: a Position object.
        Returns: True if pos is in the room, False otherwise.
        """
        x=math.floor(pos.get_x())
        y=math.floor(pos.get_y())
        if x>=0 and x<self.width:
            if y>=0 and y<self.height:
                return True 
        return False 
       

    def get_num_tiles(self):
        """
        Returns: an integer; the total number of tiles in the room
        """
        return self.width*self.height

    def get_random_position(self):
        """
        Returns: a Position object; a random position inside the room
        """
       
        random_x=random.uniform(0, self.width)
        random_y=random.uniform(0,self.height) 
        return Position(random_x, random_y)

class Robot(object):
    """
    Represents a robot cleaning a particular room.

    At all times, the robot has a particular position and direction in the room.
    The robot also has a fixed speed and a fixed cleaning_volume.

    Subclasses of Robot should provide movement strategies by implementing
    update_position_and_clean, which simulates a single time-step.
    """
    def __init__(self, room, speed, cleaning_volume):
        """
        Initializes a Robot with the given speed and given cleaning_volume in the
        specified room. The robot initially has a random direction and a random
        position in the room.

        room:  a Room object.
        speed: a positive float.
        cleaning_volume: a positive float; the amount of dust cleaned by the robot
                  in a single time-step.
        """
        self.room=room
        self.speed=speed
        self.cleaning_volume=abs(cleaning_volume)
        self.direction=random.uniform(0, 360)
        self.position=self.room.get_random_position() 

    def get_position(self):
        """
        Returns: a Position object giving the robot's position in the room.
        """
        return self.position 

    def get_direction(self):
        """
        Returns: a float d giving the direction of the robot as an angle in
        degrees, 0.0 <= d < 360.0.
        """
        return self.direction 

    def set_position(self, position):
        """
        Set the position of the robot to position.

        position: a Position object.
        """
        self.position=position 

    def set_direction(self, direction):
        """
        Set the direction of the robot to direction.

        direction: float representing an angle in degrees clockwise from north
        """
        self.direction=direction 
      

    def update_position_and_clean(self):
        """
        Simulates the passage of a single time-step.

        Moves robot to new position and cleans tile according to robot movement
        rules.
        """
        raise NotImplementedError
        # DO NOT CHANGE -- implement in subclasses
 

# === Problem 2
class BasicRobot(Robot):
    """
    A BasicRobot is a Robot with the standard movement strategy.

    At each time-step, a BasicRobot attempts to move in its current
    direction; when it would hit a wall, it *instead*
    chooses a new direction randomly.
    """
    def update_position_and_clean(self):
        """
        Simulates the passage of a single time-step.

        Calculate the next position for the robot.

        If that position is valid, move the robot to that position. Mark the
        tile it is on as having been cleaned by cleaning_volume amount.

        If the new position is invalid, do not move or clean the tile, but
        rotate once to a random new direction.
        """
         
        current_position=self.position.get_new_position(self.direction, self.speed) 
        #it shouldn't be get_new_position right?
        if self.room.is_position_in_room(current_position):
            self.room.clean_tile_at_position(current_position, self.cleaning_volume) #is cleaning_volume inherited? 
            self.set_position(current_position)
        else: 
            #get_direction returns the current direction 
            new_direction=random.random()*360 
            self.set_direction(new_direction)
            #you want the robot to move, use new direction to get new position 
            #want it to calculate the position and check if position is in the room and if so then update position 

# === Problem 3
class FaultyRobot(Robot):
    """
    A FaultyRobot is a robot that may accidentally drop dust on a tile. A FaultyRobot will drop some dust 
    on the tile it's on with probability p. 
    The amount of dropped dust should be a random decimal value between 0 and 0.5. 
    Regardless of whether the robot drops dust, it moves to a new position to clean that tile.
    If that new position is not valid, the robot just randomly changes direction.
    """
    p = 0.05

    @staticmethod
    def set_dust_probability(prob):
        """
        Sets the probability of the robot accidentally dropping dust on the tile equal to prob.

        prob: a float (0 <= prob <= 1)
        """
        FaultyRobot.p = prob

    def does_drop_dust(self):
        """
        Answers the question: Does the robot accidentally drop dust on the tile
        at this timestep?
        The robot drops dust with probability p.

        returns: True if the robot drops dust on its tile, False otherwise.
        """
        return random.random() < FaultyRobot.p

    def update_position_and_clean(self):
        """
        Simulates the passage of a single time-step.

        1. Before moving, the robot checks if it should drop dust using does_drop_dust.
            If the robot drops dust, it adds a random decimal amount of dust
            between 0 (inclusive) and 0.5 (exclusive).
            If the robot does not drop dust, it just goes to step 2.
        2. Calculate the robot's next position.
            If the position is valid, the robot cleans that tile.
            If the position is not valid, the robot randomly picks a new direction.
        """
        pos=self.position
        if self.does_drop_dust(): 
            #dust_amount=self.room.dust_amount
            extra_dust=random.random()*0.5
            self.room.clean_tile_at_position(pos, -extra_dust) #subtract negative equals adding dust 
            #update to include extra dust 
        #drop dust on the tile you are currently at 
       
        current_position=self.position.get_new_position(self.direction, self.speed) 
        if self.room.is_position_in_room(current_position):
            self.room.clean_tile_at_position(current_position, self.cleaning_volume)
            self.set_position(current_position)
        else: 
            new_direction=random.random()*360 
            self.set_direction(new_direction)

# === Problem 4
class SmartRobot(Robot):
    """
    A SmartRobot is a robot that can decide which direction to go based on the amount of dust it 
    sees.

    In one timestep, the SmartRobot will look at its surrounding area and find where there is the
    most dust. In the same timestep, it will move towards one of the positions with the most dust.

    It scans the surrounding area by checking each angles between 0 and 360.
    Naturally, many scans will return the same amount of dust, so after the robot completes it's 
    scan, it will randomly pick with uniform probability one of the angles that have the most 
    amount of dust.
    """

    def sense_dust_at_angle(self, angle):
        """
        args:
            angle (int): Angle in degrees of which direction to look

        returns:
            The amount of dust at the position the robot would end up if it moved in the direction
            of angle. Returns -1 if the position is a wall.

        DO NOT MODIFY
        """
        lookahead_pos = self.get_position().get_new_position(angle, self.speed)
        if not self.room.is_position_in_room(lookahead_pos):
            return -1

        tile = (int(lookahead_pos.get_x()), int(lookahead_pos.get_y()))
        return self.room.get_dust_amount(tile[0], tile[1])

    def scan_surrounding_area(self):
        """
        Looks at every 5th integer angle from [0, 360) and returns a dictionary mapping angle to
        dust amount.

        If the scanner sees a wall in one of the scans, it will give a reading of -1.

        DO NOT MODIFY
        """
        dust_amounts = {}
        for angle in range(0, 360, 5):
            dust_amounts[angle] = self.sense_dust_at_angle(angle)

        return dust_amounts

    def update_position_and_clean(self):
        """
        Simulates the passage of a single time-step.

        Within one time step (i.e. one call to update_position_and_clean), the robot should:

        1. Scan the surrounding area (use scan_surrounding_area)
        2. Find the angles with the maximum amount of dust
        3. Pick one of the dirtiest angles at random and move in that direction (random.choice()
           might be useful!)
        4. Clean the tile the robot lands on
        """
        max_value=0
        dirty_angles=[]
        angle_dust_dict=self.scan_surrounding_area()
        #angle picked will always be in the room because of scan_surrounding_area
        for angle, dust in angle_dust_dict.items():
            if dust>max_value: 
                max_value=angle_dust_dict[angle] #reset max value if dust>max_value
        for angle, dust in angle_dust_dict.items():
            if dust==max_value: 
                dirty_angles.append(angle) #add the angles that have maximum amount of dust 
        random_angle=random.choice(dirty_angles) #choose one random dirty angle 
        self.direction=random_angle #assigns random_angle to direction 
        #keep changing angle as you go along 
        self.position=self.position.get_new_position(self.direction, self.speed) 
        #if room.is_position_in_room(current_position):
        self.room.clean_tile_at_position(self.position, self.cleaning_volume)
       #can set position doing self.position= 
        

# === Problem 5
def run_simulation(num_robots, speed, cleaning_volume, width, height, dust_amount, min_coverage, num_trials,
                  robot_type):
    """
    Runs num_trials trials of the simulation and returns the mean number of
    time-steps needed to clean the fraction min_coverage of the room.

    The simulation is run with num_robots robots of type robot_type, each
    with the input speed and cleaning_volume in a room of dimensions width x height
    with the dust dust_amount on each tile. Each trial is run in its own Room
    with its own robots.

    num_robots: an int (num_robots > 0)
    speed: a float (speed > 0)
    cleaning_volume: a float (cleaning_volume > 0)
    width: an int (width > 0)
    height: an int (height > 0)
    dust_amount: an int
    min_coverage: a float (0 <= min_coverage <= 1.0)
    num_trials: an int (num_trials > 0)
    robot_type: class of robot to be instantiated (e.g. BasicRobot or
                FaultyRobot)
    """
    time_step_counter=0
    for i in range(num_trials): 
        room=Room(width, height, dust_amount) #create room instance object 
        robot_list=[robot_type(room, speed, cleaning_volume) for i in range(num_robots)]
        #need to initialize robot 
        #robot is the same for every single trial 
        #ten different robots
        num_tiles=room.get_num_tiles() 
        num_cleaned_tiles=room.get_num_cleaned_tiles() 
        current_coverage=num_cleaned_tiles/num_tiles 
        while current_coverage<min_coverage: #keep running loop until meet min coverage 
            num_cleaned_tiles=room.get_num_cleaned_tiles() 
            current_coverage=num_cleaned_tiles/num_tiles #recalculate current_coverage 
            for robot in robot_list: #iterate through each robot 
                robot.update_position_and_clean() 
            time_step_counter+=1 
    return time_step_counter/num_trials 






# === Problem 6
#
# ANSWER THE FOLLOWING QUESTIONS:
#
# 1)How does the performance of the three robot types compare when cleaning 80%
#       of a 20x20 room?
# When cleaning 80% of a 20x20 room, the faulty robot was the slowest followed by 
# basic robot and smart robot was the fastest. 
# Basic robot isn't much faster than faulty robot, while smart robot is much faster 
# compared to the basic robot. All three graphs are linear. 

# 2) How does the performance of the three robot types compare when two of each
#       robot cleans 80% of rooms with dimensions
#       10x30, 20x15, 25x12, and 50x6?
#  Basic robot requires the most time steps followed by faulty robot and then 
#   smart robot has the least number of steps. Like question 1, basic doesn't 
# save a lot of steps compared to faulty, whereas smart saves a lot more steps.
# As the aspect ratio increases however smart robot steps increases significantly.  

def show_plot_compare_strategies(title, x_label, y_label):
    """
    Produces a plot comparing the three robot strategies in a 20x20 room with 80%
    minimum coverage.
    """
    num_robot_range = range(1, 3)
    times1 = []
    times2 = []
    times3 = []
    for num_robots in num_robot_range:
        print ("Plotting", num_robots, "robots...")
        times1.append(run_simulation(num_robots, 1.0, 1, 20, 20, 3, 0.8, 20, BasicRobot))
        times2.append(run_simulation(num_robots, 1.0, 1, 20, 20, 3, 0.8, 20, FaultyRobot))
        times3.append(run_simulation(num_robots, 1.0, 1, 20, 20, 3, 0.8, 20, SmartRobot))
    pylab.plot(num_robot_range, times1)
    pylab.plot(num_robot_range, times2)
    pylab.plot(num_robot_range, times3)
    pylab.title(title)
    pylab.legend(('BasicRobot', 'FaultyRobot', 'SmartRobot'))
    pylab.xlabel(x_label)
    pylab.ylabel(y_label)
    pylab.show()

def show_plot_room_shape(title, x_label, y_label):
    """
    Produces a plot showing dependence of cleaning time on room shape.
    """
    aspect_ratios = []
    times1 = []
    times2 = []
    times3 = []
    for width in [10, 20, 25, 50]:
        height = int(300/width)
        print ("Plotting cleaning time for a room of width:", width, "by height:", height)
        aspect_ratios.append(float(width) / height)
        times1.append(run_simulation(2, 1.0, 1, width, height, 3, 0.8, 200, BasicRobot))
        times2.append(run_simulation(2, 1.0, 1, width, height, 3, 0.8, 200, FaultyRobot))
        times3.append(run_simulation(2, 1.0, 1, width, height, 3, 0.8, 200, SmartRobot))
    pylab.plot(aspect_ratios, times1, 'o-')
    pylab.plot(aspect_ratios, times2, 'o-')
    pylab.plot(aspect_ratios, times3, 'o-')
    pylab.title(title)
    pylab.legend(('BasicRobot', 'FaultyRobot', 'SmartRobot'), fancybox=True, framealpha=0.5)
    pylab.xlabel(x_label)
    pylab.ylabel(y_label)
    pylab.show()

if __name__ == "__main__":
    # Test code should go HERE so that test_ps3_student.py doesn't have to run it!
    # All code in this block will be run ONLY if you run ps3.py directly.

    # Uncomment this line to see your implementation of BasicRobot in action!
    #test_robot_movement(BasicRobot, Room)

    # Uncomment this line to see your implementation of FaultyRobot in action!
    #test_robot_movement(FaultyRobot, Room)
    
    # Uncomment this line to see your implementation of SmartRobot in action!
    #test_robot_movement(SmartRobot, Room)

    #show_plot_compare_strategies('Time to clean 80% of a 20x20 room, for various numbers of robots','Number of robots','Time (steps)')
    #show_plot_room_shape('Time to clean 80% of a 300-tile room for various room shapes','Aspect Ratio', 'Time (steps)')
    pass 


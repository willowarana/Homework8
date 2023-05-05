#the intial framework for a particle swarm optimization for Schwefel minimization problem
#author: Charles Nicholson
#for ISE/DSA 5113


#need some python libraries
import copy
import math
from random import Random


#to setup a random number generator, we will specify a "seed" value
seed = 12345
myPRNG = Random(seed)

#to get a random number between 0 and 1, write call this:             myPRNG.random()
#to get a random number between lwrBnd and upprBnd, write call this:  myPRNG.uniform(lwrBnd,upprBnd)
#to get a random integer between lwrBnd and upprBnd, write call this: myPRNG.randint(lwrBnd,upprBnd)

lowerBound = -500  #bounds for Schwefel Function search space
upperBound = 500   #bounds for Schwefel Function search space

#you may change anything below this line that you wish too -----------------------------------------------------

#note: for the more experienced Python programmers, you might want to consider taking a more object-oriented approach to the PSO implementation, i.e.: a particle class with methods to initialize itself, and update its own velocity and position; a swarm class with a method to iterates through all particles to call update functions, etc.

#number of dimensions of problem
dimensions = 2

#number of particles in swarm
swarmSize = 5

#number of iterations
iterations = 10

#acceleration constants
phi_1 = 1.49618
phi_2 = 1.49618

#inertia weight
w = 0.7298

#penalty for infeasibility
penalty = 10

#maximum velocity
vmax = 1000
      
#Schwefel function to evaluate a real-valued solution x    
# note: the feasible space is an n-dimensional hypercube centered at the origin with side length = 2 * 500
               
def evaluate(x):          
      val = 0
      d = len(x)
      for i in range(d):
            val = val + x[i]*math.sin(math.sqrt(abs(x[i])))
      val = 418.9829*d - val
      for i in range(d): #for each dimension
            if x[i] > 500 or x[i] < -500: #if the value is infeasible (outside of the bounds)
                  val = val + val * penalty #penalize the value
      return val          

#returns a list of velocities, one for each dimension of the particle passed
def velocity(pos, vel, pBest, gBest): #update the velocity for a certain particle
      r1 = [] #initialize first random vector
      r2 = [] #initialize second random vector
      newVels = [] #initialize updated velocities vector
      for d in range(dimensions): #for each dimension of this particle
            r1.append(myPRNG.random()) #initialize first random vector
            r2.append(myPRNG.random()) #initialize second random vectors
      for d in range(dimensions): #for each dimension of this particle
            newVel = w * vel[d] + phi_1 * r1[d] * (pBest[d] - pos[d]) + phi_2 * r2[d] * (gBest - pos[d])
            if newVel > vmax:
                  newVel = vmax
            if newVel < -vmax:
                  newVel = - vmax
            newVels.append(newVel) #compute and store its new velocity
      return newVels

#returns a list of positions, one for each dimension of the particle passed
def move(pos, vel): #update the position for a certain particle
      newPos = []  #initialize updated positions vector
      for d in range(dimensions): #for each dimension of this particle
            newPos.append(pos[d] + vel[d]) #compute and store its new position
      return newPos

#the swarm will be represented as a list of positions, velocities, values, pbest, and pbest values

pos = [[] for _ in range(swarmSize)]      #position of particles -- will be a list of lists; e.g., for a 2D problem with 3 particles: [[17,4],[-100,2],[87,-1.2]]
vel = [[] for _ in range(swarmSize)]      #velocity of particles -- will be a list of lists similar to the "pos" object 

#note: pos[0] and vel[0] provides the position and velocity of particle 0; pos[1] and vel[1] provides the position and velocity of particle 1; and so on. 


curValue = [] #evaluation value of current position  -- will be a list of real values; curValue[0] provides the evaluation of particle 0 in it's current position
pbest = []    #particles' best historical position -- will be a list of lists: pbest[0] provides the position of particle 0's best historical position
pbestVal = [] #value of pbest position  -- will be a list of real values: pbestBal[0] provides the value of particle 0's pbest location


#initialize the swarm randomly
for i in range(swarmSize):
      for j in range(dimensions):
            pos[i].append(myPRNG.uniform(lowerBound,upperBound))    #assign random value between lower and upper bounds
            vel[i].append(myPRNG.uniform(-1,1))                     #assign random value between -1 and 1   --- maybe these are good bounds?  maybe not...
            
      curValue.append(evaluate(pos[i]))   #evaluate the current position

gBest = pos[0] #initialize gBest
gBestVal = curValue[0]
pBest = pos[:]          # initialize pbest to the starting position
pBestVal = curValue[:]  # initialize pbest to the starting position

for i in range(0,iterations): #for each iteration
      for i in range(swarmSize):  # evaluate the swarm and update pBest and gBest
            curValue[i] = evaluate(pos[i]) #update curValue
            if curValue[i] < pBestVal[i]: #update pBest for current particle
                  pBest[i] = pos[i]
                  pBestVal[i] = curValue[i]
            if curValue[i] < gBestVal: #update gBest
                  gBest = pos[i]
                  gBestVal = curValue[i]
      for i in range(swarmSize): #for each particle
            vel[i] = velocity(pos[i],vel[i], pBest[i], gBestVal) #update velocity
            pos[i] = move(pos[i], vel[i]) #update position
print("Best position: ", gBest)
print("Best value: ", gBestVal)
#Currently missing several elements
#e.g., velocity update function; velocity max limitations; position updates; dealing with infeasible space; identifying the global best; main loop, stopping criterion, etc. 
                                                                          



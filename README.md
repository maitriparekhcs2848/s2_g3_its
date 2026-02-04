+**Bus Routing Probability School Routing and Stop Selecting.
Project Overview**

The research question that is to be answered in the project will be the solution of the School Bus Routing Problem with Stop Selection based on a probabilistic optimisation tool. It is to determine an optimal combination of bus stops, assign students to the possible bus stops as well as determine the optimum order of routes which will take minimum time in the case of uncertainty.

School Bus Routing Problem with Stop Selection includes selecting the optimum bus stops, assigning the students to the nearest feasible bus stops, and identifying the optimal sequence of routes to save the total time of traveling with the constraint of walking distance and bus capacity. The probabilistic optimization method based on an Estimation of Distribution Algorithm (EDA) is used to learn and generate efficient routes due to the size of the possible combination of routes.

**Objectives**

Optimize the distance of walking-model of the student-to-stop problems.
Bring uncertainty to the travelling, to the route choice.
The dominant random variables of routing system are established.
Probability based learning of EDA.
Find the optimal routes that have the shortest time expected to take.

**Key Concepts**

Random Variables
Probability Distributions
Stochastic Sampling
Uncertainty Optimization.
Estimation of Distribution Algorithm (EDA)

**System Components**

Students Locations
Potential Bus Stops
Distance Feasibility Matrix.
Student–Stop Assignments
Road Network and Travel Time

**Sources of Uncertainty**

The randomly spatially placed students.
Different traffic that influences the travelling time.
Several work visits to the student.
Large magnitudes of routes combinations.

**Random Variables**

RV1: The identification of every student.
RV 2: List of stops (course) that are to be visited.
RV3: Total travel time of route

**Probabilistic Approach**

The Estimation of Distribution Algorithm (EDA) operates in the following way: original routes are produced, their performance in successful routes are selected, probability distributions are estimated with regards to these routes, and improved routes are sampled. This is achieved in an instance where the optimum routing solution is not stopped.

**Workflow**

Create student and stop data.
Build feasibility matrix
Assign students to stops
Construct feasible routes
Evaluate travel time
Get to know the probability distributions.
Sample improved routes
Repeat until convergence

**Outcome**

This project has shown that, the probabilistic models, and optimization through the use of learning could have been used to minimize the travel time and the uncertainty in the transportation routing system.

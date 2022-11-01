# Grouping-optimization
This website is intended to achieve the fairest group division, increasing overall satisfaction of groupmates.
https://group-optipus.herokuapp.com

## Features
To work with the algorithms, an account is needed.
- Users can register accounts on group-optipus.herokuapp.com. In every account, user can join a classroom or create a new one. 
- Classrooms are intended for the class owner (the class creator) to select the favorite algorithm to generate optimized groups. There is an algorithm is faster for smaller classes (less than 12 people), and the other that is generally slower but capable of handling larger classes.
- Everyone except the class owner have the interface to provide information of their favorites as well as someone they do not like much. The information is designed not be exposed to anyone within and outside the classroom. Only the person holding the information can view it.
- The web application supports both English and Traditional Chinese.


## Algorithms
The web application actually includes only Combination Selection Grouping and Regression Algorithm, but three algorithms were developed just in case if they are useful.

### 1. Combination Selection Grouping
1. The possible outcome of a single groups are generated using itertools library.
2. Using a recursive function, compute the possible outcomes of other groups to form nCr cases, which n is the number of people in total, and r is the group size.
3. A dictionary of people favorism are used to compute the overall happiness of each group. For every groupmates, if one favored person in the same group, the overall happiness index will plus 1. On the other hand, if one unfavored person in the same group, the overall happiness index will minus 1.
4. The happiness calculation will run in every groups in every cases
5. The score of least happy groups will be collected as a list, where each element represent the least happy group of each case.
6. The cases with highest least happy score will be selected to be the output.

### 2. Regression Algorithm
1. The program generates the groups randomly
2. The program calculates the most unhappy group, and change the member from the group with other groups randomly. The happiness calculation algorithm is the same as that of Combination Selection Grouping
3. If the score of the most unhappy group exceeds the record, then set it as the current record. If the program cannot beat the record with a fixed attempts, the program will return the record.

### 3. Branch Grouping (not implemented)
1. A collection of targets of favor are the collection of all members for grouping.
<img src="images/Original.png" width=500px>
1. Each member is wanted by several other people, branching out from the target.
2. A branch is selected randomly from the collection.
3. To select people with the target, the algorithm start to select the member who likes the target with a fewer branches.
4. If a branch is selected, the target is not available for grouping anymore.
5. If running out of liked members (branches), looking for the branch that the target is the in one of branches of the branch. If not available, then the algorithm will randomly assign group members into the group.
#### See the pictures for better understanding

<img src="images/Original.png" width=500px>
<img src="images/First_selection.png" width=500px>
<img src="images/First_BS.png" width=500px>
<img src="images/Group_BS.png" width=500px>
<img src="images/Second_selection.png" width=500px>
<img src="images/Group_BS2.png" width=500px>
<img src="images/Third_selection.png" width=500px>
<img src="images/Forth_selection.png" width=500px>
<img src="images/done.png" width=500px>

## Performance
### Complexity for Combination Selection Grouping:
n represents the total number of people, r represents the group size, and x represents a positive integer.
<br/>
### $O={n-1 \choose r-1} \cdot {n-r-1 \choose r-1} \cdot {n-2r-1 \choose r-1}...;n-xr-1 \geq r-1$
The complexity grows factorially. Therefore, it is not suitable to group a class with more than 12 people.

### Complexity for Regression Algorithm:
Maximum complexity: <br/>
### $O = depth * attempts$<br/>
whereas depth is set fixed to 100 and maximum attempts is set fixed to 100000.<br/>
Therefore, it is more usable when grouping large classes.







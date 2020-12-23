# Grouping-optimization

Two algorithms are used to optimize grouping and improve overall groupmate happiness
https://group-optipus.herokuapp.com


## 1. Branch grouping
1. A collection of targets of favor are the collection of all members for grouping.
![](images/Original.png)
1. Each member is wanted by several other people, branching out from the target.
2. A branch is selected randomly from the collection.
3. To select people with the target, the algorithm start to select the member who likes the target with a fewer branches.
4. If a branch is selected, the target is not available for grouping anymore.
5. If running out of liked members (branches), looking for the branch that the target is the in one of branches of the branch. If not available, then the algorithm will randomly assign group members into the group.
### See the pictures for better understanding

![](images/Original.png)
![](images/First_selection.png)
![](images/First_BS.png)
![](images/Group_BS.png)
![](images/Second_selection.png)
![](images/Group_BS2.png)
![](images/Third_selection.png)
![](images/Forth_selection.png)
![](images/done.png)
## 2. Combination grouping
1. The possible outcome of a single groups are generated using itertools library.
2. Using a recursive function, compute the possible outcomes of other groups to form nCr cases, which n is the number of people in total, and r is the group size.
3. A dictionary of people favorism are used to compute the overall happiness of each group. For every groupmates, if one favored person in the same group, the overall happiness index will plus 1. On the other hand, if one unfavored person in the same group, the overall happiness index will minus 1.
4. The happiness calculation will run in every groups in every cases
5. The difference of the most happy group and the least happy group is calculated and recorded on a list.
6. The cases with least difference in happiness will be selected to be the output.


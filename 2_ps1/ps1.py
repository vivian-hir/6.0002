################################################################################
# 6.100B Spring 2023
# Problem Set 1
# Name: Vivian Hir 
# Collaborators: None 
# Time: 6:00 

from state import State

##########################################################################################################
## Problem 1
##########################################################################################################

def load_election(filename):
    """
    Reads the contents of a file, with data given in the following tab-separated format:
    State[tab]Democrat_votes[tab]Republican_votes[tab]EC_votes

    Please ignore the first line of the file, which are the column headers, and remember that
    the special character for tab is '\t'

    Parameters:
    filename - the name of the data file as a string

    Returns:
    a list of State instances
    """
    file=open(filename, "r") #should I use with open? do something wrapper to read the file 
    #write a while loop, know certain condtions, more about the file 
    final_list=[]
    while file:
        line=file.readline()
        final_list.append(line)
        if line =="":
            break
    file.close()
    final_list=final_list[1:-1]
    formatted_list=[]
    state_obj_list=[]
    for state in final_list: 
        new_state=state.replace('\n', '') #delete \n replace with empty string 
        new_state=new_state.split('\t')
        formatted_list.append(new_state)
    for obj in formatted_list:
        new_state=State(obj[0], int(obj[1]), int(obj[2]), int(obj[3])) #create the state object, store them in new_list
        state_obj_list.append(new_state)
    return state_obj_list
    


##########################################################################################################
## Problem 2: Helper functions
##########################################################################################################

def election_winner(election_states):
    """
    Finds the winner of the election based on who has the most amount of EC votes.
    Note: In this simplified representation, all of EC votes from a state go
    to the party with the majority vote.

    Parameters:
    election_states - a list of State instances

    Returns:
    a tuple, (winner, loser) of the election i.e. ('dem', 'rep') if Democrats won, else ('rep', 'dem')
    """
    total_dem=0
    total_rep=0
    for state in election_states: 
        winner=state.get_winner()
        ec=state.get_ecvotes() 
        if winner=='dem':
            total_dem+=ec
        else:
            total_rep+=ec 
    if total_dem>total_rep:
        return ('dem', 'rep')
    else:
        return ('rep', 'dem')
    


def get_winning_states(election_states):
    """
    Finds the list of States that were won by the winning candidate (lost by the losing candidate).

    Parameters:
    election_states - a list of State instances

    Returns:
    A list of State instances won by the winning candidate
    """
    winning_party=election_winner(election_states)[0]
    winning_list=[]
    for state in election_states: 
        winner=state.get_winner()
        if winner==winning_party:
            winning_list.append(state)
    return winning_list
   


def ec_votes_to_flip(election_states, total=538):
    """
    Finds the number of additional EC votes required by the loser to change election outcome.
    Note: A party wins when they earn half the total number of EC votes plus 1.

    Parameters:
    election_states - a list of State instances
    total - total possible number of EC votes

    Returns:
    int, number of additional EC votes required by the loser to change the election outcome
    """
    winning_party=election_winner(election_states)[0]
    loser_votes=0
    for state in election_states: 
        winner=state.get_winner()
        if winner!=winning_party:
            ec=state.get_ecvotes()
            loser_votes+=ec
    extra_votes=total//2+1-loser_votes
    return extra_votes 
    


##########################################################################################################
## Problem 3: Brute Force approach
##########################################################################################################

def combinations(L):
    """
    Helper function to generate powerset of all possible combinations
    of items in input list L. E.g., if
    L is [1, 2] it will return a list with elements
    [], [1], [2], and [1,2].

    DO NOT MODIFY THIS.

    Parameters:
    L - list of items

    Returns:
    a list of lists that contains all possible
    combinations of the elements of L
    """

    def get_binary_representation(n, num_digits):
        """
        Inner function to get a binary representation of items to add to a subset,
        which combinations() uses to construct and append another item to the powerset.

        DO NOT MODIFY THIS.

        Parameters:
        n and num_digits are non-negative ints

        Returns:
            a num_digits str that is a binary representation of n
        """
        result = ''
        while n > 0:
            result = str(n%2) + result
            n = n//2
        if len(result) > num_digits:
            raise ValueError('not enough digits')
        for i in range(num_digits - len(result)):
            result = '0' + result
        return result

    powerset = []
    for i in range(0, 2**len(L)):
        binStr = get_binary_representation(i, len(L))
        subset = []
        for j in range(len(L)):
            if binStr[j] == '1':
                subset.append(L[j])
        powerset.append(subset)
    return powerset


def brute_force_swing_states(winner_states, ec_votes_needed):
    """
    Finds a subset of winner_states that would change an election outcome if
    voters moved into those states, these are our swing states. Iterate over
    all possible move combinations using the helper function combinations(L).
    Return the move combination that minimises the number of voters moved. If
    there exists more than one combination that minimises this, return any one of them.

    Parameters:
    winner_states - a list of State instances that were won by the winning candidate
    ec_votes_needed - int, number of EC votes needed to change the election outcome

    Returns:
    * A tuple containing the list of State instances such that the election outcome would change if additional
      voters relocated to those states, as well as the number of voters required for that relocation.
    * A tuple containing the empty list followed by zero, if no possible swing states.
    """
    #initialize variables to hold the best combo and the minimum voters moved *so far*
    best_combo, minimum_so_far= [], float("inf") #initialize something very big 
#find possible_move_combinations using helper function "combinations"
    possible_move_combinations=combinations(winner_states)
    for combo in possible_move_combinations: 
        new_ec_votes=0
        voters_moved= 0
        for item in combo: 
            margin=item.get_margin()+1 
            voters_moved+=margin 
            ec_votes=item.get_ecvotes() 
            new_ec_votes+=ec_votes  
        if new_ec_votes >= ec_votes_needed and voters_moved < minimum_so_far: 
            best_combo= combo
            minimum_so_far= voters_moved 
    if best_combo==[]:
        return [], 0
    return best_combo, minimum_so_far 


##########################################################################################################
## Problem 4: Dynamic Programming
## In this section we will define two functions, max_voters_moved and min_voters_moved, that
## together will provide a dynamic programming approach to find swing states. This problem
## is analagous to the complementary knapsack problem, you might find Lecture 1 of 6.100B useful
## for this section of the pset.
##########################################################################################################


def max_voters_moved(winner_states, max_ec_votes, memo=None):
    """
    Finds the largest number of voters needed to relocate to get at most max_ec_votes
    for the election loser.

    Analogy to the knapsack problem:
        Given a list of states each with a weight(ec_votes) and value(margin+1),
        determine the states to include in a collection so the total weight(ec_votes)
        is less than or equal to the given limit(max_ec_votes) and the total value(voters displaced)
        is as large as possible.

    Parameters:
    winner_states - a list of State instances that were won by the winner
    max_ec_votes - int, the maximum number of EC votes

    Returns:
    * A tuple containing the list of State instances such that the maximum number of voters need to
      be relocated to these states in order to get at most max_ec_votes, and the number of voters
      required required for such a relocation.
    * A tuple containing the empty list followed by zero, if every state has a # EC votes greater
      than max_ec_votes.
    """
    if winner_states==[]:
        return [], 0
    if memo==None: 
        memo = {}
    if (len(winner_states), max_ec_votes) in memo:
        return memo[len(winner_states), max_ec_votes] #does the memoization 
    current_winner=winner_states[0]
    if current_winner.get_ecvotes() > max_ec_votes: #explores the right branch only 
        solution, value = max_voters_moved(winner_states[1:], max_ec_votes, memo)
    else: #explores the left branch 
        other_soln, other_val = max_voters_moved(winner_states[1:], max_ec_votes-current_winner.get_ecvotes(), memo)
        other_soln= other_soln + [current_winner]
        other_val += current_winner.get_margin()+1 
        soln_without, val_without= max_voters_moved(winner_states[1:], max_ec_votes, memo) #explores right branch 
        solution, value = (other_soln, other_val) if other_val > val_without else (soln_without, val_without) #choose the better branch 
    memo[(len(winner_states), max_ec_votes)]= solution, value
    if winner_states == []:
        return [], 0
    return solution, value 
#supposed to calculate the margin and then add it each time to part of the solution 


def min_voters_moved(winner_states, ec_votes_needed):
    """
    Finds a subset of winner_states that would change an election outcome if
    voters moved into those states. Should minimize the number of voters being relocated.
    Only return states that were originally won by the winner (lost by the loser)
    of the election.

    Hint: This problem is simply the complement of max_voters_moved. You should call
    max_voters_moved with ec_vote_limit set to (#ec votes won by original winner - ec_votes_needed)

    Parameters:
    winner_states - a list of State instances that were won by the winner
    ec_votes_needed - int, number of EC votes needed to change the election outcome

    Returns:
    * A tuple containing the list of State instances (which we can call swing states) such that the
      minimum number of voters need to be relocated to these states in order to get at least
      ec_votes_needed, and the number of voters required for such a relocation.
    * * A tuple containing the empty list followed by zero, if no possible swing states.
    """
    #minimize the margin need to win 
    #if you want to move to tie it would be a split in electoral college votes 
    #so wouldn't the ec_vote_limit be equal to 0 then because winner=270, ec_votes_needed is 270? 
    swing_states= winner_states.copy() 
    margin_total=0 
    winner_ec_votes=0
    for winner in winner_states:
        winner_ec_votes+=winner.get_ecvotes() #get total ec votes 
    ec_vote_limit=winner_ec_votes-ec_votes_needed #get the complement value 
    solution, value= max_voters_moved(winner_states, ec_vote_limit) #calculate with ec_vote_limit 
    #states in max_voters_moved are the ones with biggest differences (non-swing) 
    for state in solution: 
        swing_states.remove(state) #remove non-swing states 
    for name in swing_states: 
        value=name.get_margin()
        margin_total+=(value+1)  #recalculate margin using only swing states 
    if swing_states== []: 
        return [], 0
    return swing_states, margin_total
    



##########################################################################################################
## Problem 5
##########################################################################################################


def relocate_voters(election_states, swing_states, ideal_states = ['AL', 'AZ', 'CA', 'TX']):
    """
    Finds a way to shuffle voters in order to flip an election outcome. Moves voters
    from states that were won by the losing candidate (states not in winner_states), to
    each of the states in swing_states. To win a swing state, you must move (margin + 1)
    new voters into that state. Any state that voters are moved from should still be won
    by the loser even after voters are moved. Also finds the number of EC votes gained by
    this rearrangement, as well as the minimum number of voters that need to be moved.
    Note: You cannot move voters out of Alabama, Arizona, California, or Texas.

    Parameters:
    election_states - a list of State instances representing the election
    swing_states - a list of State instances where people need to move to flip the election outcome
                   (result of min_voters_moved or brute_force_swing_states)
    ideal_states - a list of Strings holding the names of states where residents cannot be moved from
                   (default states are AL, AZ, CA, TX)

    Return:
    * A tuple that has 3 elements in the following order:
        - an int, the total number of voters moved
        - an int, the total number of EC votes gained by moving the voters
        - a dictionary with the following (key, value) mapping:
            - Key: a 2 element tuple of str, (from_state, to_state), the 2 letter State names
            - Value: int, number of people that are being moved
    * None, if it is not possible to sway the election
    """
    total_to_move=0
    total=0
    gained_ec_votes=0
    relocate_dict= {} 
    winning_states=get_winning_states(election_states)
    losing_candidate_states=[state for state in election_states if state not in winning_states and state.get_name() not in ideal_states]

    for state in swing_states:
        votes_to_swing=state.get_margin()+1 
        ec_votes=state.get_ecvotes()
        total_to_move+=votes_to_swing
        total+=total_to_move
        gained_ec_votes+=ec_votes 
        for name in losing_candidate_states:
            #if losing candidate state can be moved
            if total_to_move==0:
                break 
            if name.get_margin()==1: 
                continue  #go on to the next iteration of the for loop 
            votes_from_loser=name.get_margin()-1 
            actual_votes_moved=min(total_to_move, votes_from_loser)
            name.subtract_winning_candidate_voters(actual_votes_moved)
            state.add_losing_candidate_voters(actual_votes_moved)
            relocate_dict[(name.get_name(), state.get_name())]=actual_votes_moved 
            total_to_move-=actual_votes_moved
    if total_to_move!=0:
        return None 
    return total, gained_ec_votes, relocate_dict 
        


if __name__ == "__main__":
    pass
    # Uncomment the following lines to test each of the problems

    # # # tests Problem 1
    year = 2012
    election_states = load_election(f"{year}_results.txt")
    print(election_states[0])

    
    # # # tests Problem 2
    # winner, loser = election_winner(election_states)
    # won_states = get_winning_states(election_states)
    # names_won_states = [state.get_name() for state in won_states] #attribute error 
    # reqd_ec_votes = ec_votes_to_flip(election_states)
    # print("Winner:", winner, "\nLoser:", loser)
    # print("States won by the winner: ", names_won_states)
    # print("EC votes needed:",reqd_ec_votes, "\n")

    # # # tests Problem 3
    # # brute_election = load_election("6100B_results.txt")
    # # brute_won_states = get_winning_states(brute_election)
    # # brute_ec_votes_to_flip = ec_votes_to_flip(brute_election, total=14)
    # # brute_swing, voters_brute = brute_force_swing_states(brute_won_states, brute_ec_votes_to_flip)
    # # names_brute_swing = [state.get_name() for state in brute_swing]
    # # ecvotes_brute = sum([state.get_ecvotes() for state in brute_swing])
    # # print("Brute force swing states results:", names_brute_swing)
    # # print("Brute force voters displaced:", voters_brute, "for a total of", ecvotes_brute, "Electoral College votes.\n")

    # # # tests Problem 4a: max_voters_moved
    # # print("max_voters_moved")
    # # total_lost = sum(state.get_ecvotes() for state in won_states)
    # # non_swing_states, max_voters_displaced = max_voters_moved(won_states, total_lost-reqd_ec_votes)
    # # non_swing_states_names = [state.get_name() for state in non_swing_states]
    # # max_ec_votes = sum([state.get_ecvotes() for state in non_swing_states])
    # # print("States with the largest margins (non-swing states):", non_swing_states_names)
    # # print("Max voters displaced:", max_voters_displaced, "for a total of", max_ec_votes, "Electoral College votes.", "\n")

    # # # tests Problem 4b: min_voters_moved
    # # print("min_voters_moved")
    # swing_states, min_voters_displaced = min_voters_moved(won_states, reqd_ec_votes)
    # #if it is a tie then reqd_ec_votes=269 for a tie 
    # swing_state_names = [state.get_name() for state in swing_states]
    # swing_ec_votes = sum([state.get_ecvotes() for state in swing_states])
    # # print("Complementary knapsack swing states results:", swing_state_names)
    # # print("Min voters displaced:", min_voters_displaced, "for a total of", swing_ec_votes, "Electoral College votes. \n")
  
    # # # tests Problem 5: relocate_voters
    # print("relocate_voters")
    # flipped_election = relocate_voters(election_states, swing_states)
    # print("Flip election mapping:", flipped_election)

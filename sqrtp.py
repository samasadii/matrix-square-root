def is_valid_permutation(in_perm):
    """
    A permutation is a list of 2 lists of same size:
    a = [[1,2,3], [2,3,1]]
    means permute 1 with 2, 2 with 3, 3 with 1.
    :param in_perm: input permutation.
    """
    if not len(in_perm) == 2:
        return False
    if not len(in_perm[0]) == len(in_perm[1]):
        return False
    if not all(isinstance(n, int) for n in in_perm[0]):
        return False
    if not all(isinstance(n, int) for n in in_perm[1]):
        return False
    if not set(in_perm[0]) == set(in_perm[1]):
        return False
    return True



def lift_list(input_list):
    """
    List of nested lists becomes a list with the element exposed in the main list.
    :param input_list: a list of lists.
    :return: eliminates the first nesting levels of lists.
    E.G.
    >> lift_list([1, 2, [1,2,3], [1,2], [4,5, 6], [3,4]])
    [1, 2, 1, 2, 3, 1, 2, 4, 5, 6, 3, 4]
    """
    if input_list == []:
        return []
    else:
        return lift_list(input_list[0]) + (lift_list(input_list[1:]) if len(input_list) > 1 else []) \
            if type(input_list) is list else [input_list]



def decouple_permutation(perm):
    """
    from [[1, 2, 3, 4, 5], [3, 4, 5, 2, 1]]
    to   [[1,3], [2,4], [3,5], [4,2], [5,1]]
    """

    return [a for a in [list(a) for a in zip(perm[0], perm[1]) if perm[0] != perm[1]] if a[0] != a[1]]


def merge_decoupled_permutation(decoupled):
    """
    From [[1,3], [2,4], [3,5], [4,2], [5,1]]
    to   [[1, 3, 5], [2, 4]]
    """
    ans = []
    while len(decoupled):
        index_next = [k[0] for k in decoupled[1:]].index(decoupled[0][-1]) + 1
        decoupled[0].append(decoupled[index_next][1])
        decoupled.pop(index_next)
        if decoupled[0][0] == decoupled[0][-1]:
            ans.append(decoupled[0][:-1])
            decoupled.pop(0)
    return ans


def from_permutation_to_disjoints_cycles(a):
    """
    from [[1, 2, 3, 4, 5], [3, 4, 5, 2, 1]]
    to   [[1, 3, 5], [2, 4]]
    """
    perm = []
    b = []
    for i in range(len(a)):
        b.append(i)

    perm.append(b)
    perm.append(a)

    if not is_valid_permutation(perm):
        raise IOError('Input permutation is not valid')
    temp = merge_decoupled_permutation(decouple_permutation(perm))

    for i in range(len(a)):
        if (i == a[i]):
            temp.append([i])
    
    return temp


def from_disjoint_cycles_to_permutation(dc, n):
    
    result = [-1] * n
    for cycle in dc:
        cycle_len = len(cycle)
        i = 0
        while (i < cycle_len):
            if (i == cycle_len - 1):
                result[cycle[i]] = cycle[0]
            else:
                result[cycle[i]] = cycle[i + 1]
            i += 1
        
    return result


def divide_lists(cycles):
    evens = []
    odds = []
    result = []

    for cycle in cycles:
        if ((len(cycle) % 2) == 0):
            evens.append(cycle)
        else:
            odds.append(cycle)

    evens.sort(key=len)
    odds.sort(key=len)

    result.append(evens)
    result.append(odds)

    return result

def check_possibility_evens(evens_list):
    n = len(evens_list)
    i = 0
    if (len(evens_list) % 2 == 1):
        return False
    while (i < n):
        if (len(evens_list[i]) != len(evens_list[i+1])):
            return False
        i += 2
    
    return True

def divide_odds(odds_list):
    n = len(odds_list)
    evens = []
    odds = []
    result = []
    i = 0
    while (i < n):
        if (i+1 < n):
            if(len(odds_list[i]) == len(odds_list[i+1])):
                evens.append(odds_list[i])
                evens.append(odds_list[i+1])
                i += 2
            else:
                odds.append(odds_list[i])
                i += 1
        else:
            odds.append(odds_list[i])
            i += 1

    result.append(evens)
    result.append(odds)

    return result

def merge(cycle):
    n = len(cycle)
    i = 0
    result = []
    while (i < n):
        temp = []
        cycle_len = len(cycle[i])
        j = 0
        while (j < cycle_len):
            temp.append(cycle[i][j])
            temp.append(cycle[i+1][j])
            j += 1
        i += 2
        result.append(temp)

    return result

def merge_odd(cycle):
    n = len(cycle)
    i = 0
    result = []
    while (i < n):
        temp = []
        cycle_len = len(cycle[i])
        j = 1
        temp.append(cycle[i][0])
        while(j < (cycle_len/2)):
            temp.append(cycle[i][int(cycle_len/2) + j])
            temp.append(cycle[i][j])
            j += 1
        i += 1
        result.append(temp)

    return result

def add_list(y, x):
    for i in x:
        y.append(i)
    return y



def run(permutation, size):

    cycles = from_permutation_to_disjoints_cycles(permutation)
    divided_cycles = divide_lists(cycles)
    if (check_possibility_evens(divided_cycles[0])):
        result = []
        divided_cycles.append(divide_odds(divided_cycles.pop(1)))
        tmp = []
        tmp = merge(divided_cycles[0])
        result = add_list(result, tmp)
        tmp = merge(divided_cycles[1][0])
        result = add_list(result, tmp)
        tmp = merge_odd(divided_cycles[1][1])
        result = add_list(result, tmp)

        print(from_disjoint_cycles_to_permutation(result, size))
    else:
        print ('impossible')

def get_input():
    n = int(input())
    for i in range(n):
        size = int(input())
        permutation = input().split(' ')
        j = 0
        while (j < size):
            permutation[j] = int(permutation[j])
            j += 1
        run(permutation, size)

get_input()
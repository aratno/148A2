import math

n = 10
print("#n: {}".format(n))

def list_moves(state):
    output = []
    output.extend([i**2 for i in range(1, math.floor(math.sqrt(state)) + 1)])
    return output

def get_states(state):
    output = []
    output.extend(state - i for i in list_moves(state))
    return output

print("L: {}".format(list_moves(n)))
print("S: {}\n".format(get_states(n)))

def replace_list(L):
    if isinstance(L, list):
        print(L)
        return [replace_list(x) for x in L]
    else:
        print(L)
        #return [get_states for x in get_states(L)]
        return get_states(L)

replace_list(n)

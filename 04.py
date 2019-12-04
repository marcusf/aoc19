def is_valid(ztr):
    is_ascending = ''.join(sorted(list(ztr))) == ztr
    if not is_ascending:
        return False

    for i in range(len(ztr)-1):
        if ztr[i] == ztr[i+1]: 
            return True

    return False

def repeats_twice(cand):
    ll = [1]
    idx = 0
    s = str(cand)
    for i in range(len(s)-1):
        if s[i] == s[i+1]:
            ll[idx] += 1
        else:
            ll.append(1)
            idx += 1
    return 2 in ll

start, end = [int(i) for i in '245182-790572'.split('-')]

candidates = []

for num in range(start, end+1):
    if is_valid(str(num)): 
       candidates.append(num)

# Task 1
print(len(candidates))

scrubbed = []

for cand in candidates:
    if repeats_twice(cand):
        scrubbed.append(cand)

print(len(scrubbed))
    
s='R6,L10,R8,R8,R12,L8,L8,R6,L10,R8,R8,R12,L8,L8,L10,R6,R6,L8,R6,L10,R8,R8,R12,L8,L8,L10,R6,R6,L8,R6,L10,R8,L10,R6,R6,L8'.split(',')

def split(ss):
    st = [[s[0],s[1:]] for s in ss]
    return [a for s in st for a in s]

def compress(s):
    for a in range(2,6):
        a_subset = s[0:a]
        ss = []
        j = 0
        while j < len(s):
            if s[j:(j+a)] == a_subset:
                ss.append('A')
                j += a
            else:
                ss.append(s[j])
                j += 1
        #print(ss)

        for b in range(2,6):
            b_subset = ss[1:1+(max(b,ss.index('A')))]
            sb = []
            k = 0
            while k < len(ss):
                if ss[k:(k+b)] == b_subset:
                    sb.append('B')
                    k += b
                else:
                    sb.append(ss[k])
                    k += 1

            cs, ce = 0, 0
            for q, c in enumerate(sb):
                if not c in ('A','B'):
                    if cs == 0:
                        cs = q
                        break
            ce = cs
            while not sb[ce] in ('A','B'):
                ce += 1

            c_subset = sb[cs:ce]

            clen = ce-cs

            sc = []
            l = 0

            while l < len(sb):
                if sb[l:l+clen] == c_subset:
                    sc.append('C')
                    l += clen
                else:
                    sc.append(sb[l])
                    l += 1

            found = True
            for c in sc:
                if c not in ('A','B','C'):
                    found = False
            if found:
                return [",".join(sc)+"\n",
                ",".join(split(a_subset))+"\n",
                ",".join(split(b_subset))+"\n", 
                ",".join(split(c_subset))+"\n"]

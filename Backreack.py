from Parse import Parse

def match_backreace(node, r, idx):
    if node is None:
        yield idx
    elif node == '.':
        if idx < len(r):
            yield idx + 1
    elif isinstance(node, str) and len(node) == 1:
        if idx < len(r) and r[idx] == node:
            yield idx + 1
    elif node[0] == '|':
        yield from match_backreace(node[1], r, idx)
        yield from match_backreace(node[2], r, idx)
    elif node[0] == '&':
        yield from match_and(node, r, idx)
    elif node[0] == 'postfix':
        yield from match_postfix(node, r, idx)
    else:
        raise Exception("backtrace have something wrong " + node[0])
def match_and(node, r, idx):
    s = set()
    for i in match_backreace(node[1], r, idx):
        if i not in s:
            s.add(i)
            yield from match_backreace(node[2], r, i)
def match_postfix(node, r, idx):
    _, ch, minn, maxn = node
    st = set()
    st.add(idx)
    ans = []
    if minn == 0:
        ans.append(idx)
    for i in range(1, maxn + 1):
        ss = set()
        for j in st:
            for k in match_backreace(ch, r, j):
                if k > len(r):
                    continue
                if k < len(r):
                    ss.add(k)
                if i >= minn:
                    ans.append(k)
        if len(ss) == 0:
            break
        st = ss
    yield from ans 
def match(regex, text):
    node = Parse.parse(regex)
    for i in match_backreace(node, text, 0):
        if i == len(text):
            return True
    return False
if __name__ == "__main__":
    assert(match("a|b", "a") == True)
    assert(match("a|b", "b") == True)
    assert(match("a|b", "c") == False)
    assert(match("a|b|c", "a") == True)
    assert(match("a|b|c", "b") == True)
    assert(match("a|b|c", "c") == True)
    assert(match("a|b|c", "d") == False)
    assert(match("a*", "a") == True)
    assert(match("a+", "") == False)
    assert(match("a*", "") == True)
    assert(match("a*", "a") == True)
    assert(match("a*", "aa") == True)
    assert(match("abc", "ac") == False)
    assert(match("abc", "ab") == False)
    assert(match("abc", "abc") == True)
    assert(match("abc", "abcc") == False)
    assert(match("abc|def", "abc") == True)
    assert(match("abc|def", "def") == True)
    assert(match("abc|def", "ab") == False)
    assert(match("abc|def", "de") == False)
    assert(match("a{3,8}", "aaaaa") == True)
    assert(match("a{3,8}", "aaa") == True)
    assert(match("a{3,8}", "a") == False)
    assert(match("a{3,8}", "aa") == False)
    assert(match("a{3,8}", "aaaa") == True)
    assert(match("a{3,8}", "aaaaaa") == True)
    assert(match("a{3,8}", "aaaaaaa") == True)
    assert(match("a{3,8}", "aaaaaaaa") == True)
    assert(match("a{3,8}", "aaaaaaaaa") == False)
from Parse import Parse

def make_graph(node, start, end, id2node):
    if node is None:
        start.append((None, end))
    elif node == '.':
        start.append(('.', end))
    elif isinstance(node, str):
        start.append((node, end))
    elif node[0] == '&':
        mid = []
        id2node[id(mid)] = mid
        make_graph(node[1], start, mid, id2node)
        make_graph(node[2], mid, end, id2node)
    elif node[0] == '|':
        make_graph(node[1], start, end, id2node)
        make_graph(node[2], start, end, id2node)
    elif node[0] == "postfix":
        make_postfix(node, start, end, id2node)

def make_postfix(node, start, end, id2node):
    _, node, minn, maxn = node
    din = []
    dout = ('boss', din, end, minn, maxn)
    id2node[id(din)] = din
    id2node[id(dout)] = dout
    make_graph(node, din, dout, id2node)
    start.append((None, din))
    if minn == 0:
        start.append((None, end))
def match(regex, text):
    node = Parse.parse(regex)
    start = []
    end = []
    id2node = {}
    id2node[id(start)] = start
    id2node[id(end)] = end
    make_graph(node, start, end, id2node)
    node_set = {(id(start), ())}
    match_free(node_set, id2node)
    for ch in text:
        node_set = match_step(node_set, id2node, ch)
        match_free(node_set, id2node)
    return (id(end), ()) in node_set
def match_free(node_set, id2node):
    start = list(node_set)
    while start:
        new_nodes = []
        for idd, kv in start:
            node = id2node[idd]
            if isinstance(node, tuple) and node[0] == 'boss':
                node_set.remove((id(node), kv))
                for dst, kv in match_boss(node, kv):
                    new_nodes.append((id(dst), kv))
            else:
                for cond, dst in node:
                    if cond is None:
                        new_nodes.append((id(dst), kv))
        start = []
        for state in new_nodes:
            if state not in node_set:
                node_set.add(state)
                start.append(state)
def match_boss(node, kv):
    _, din, end, minn, maxn = node
    key = id(din)
    kv, cnt = kv_increase(kv, key)
    if cnt < maxn:
        yield (din, kv)
    if minn <= cnt <= maxn:
        yield (end, kv_delete(kv, key))
def kv_increase(kv, key):
    kv = dict(kv)
    val = kv.get(key, 0) + 1
    kv[key] = val
    return tuple(sorted(kv.items())), val

def kv_delete(kv, key):
    return tuple((k, v) for k, v in kv if k != key)
def match_step(node_set, id2node, ch):
    nodeset = set()
    for idd, kv in node_set:
        node = id2node[idd]
        for c, next_node in node:
            if c == '.' or c == ch:
                nodeset.add((id(next_node), kv))
    return nodeset
def debug(regex, text):
    # print(regex)
    node = Parse.parse(regex)
    print(node)
    id2node = {}
    start = []
    end = []
    id2node[id(start)] = start
    id2node[id(end)] = end
    make_graph(node, start, end, id2node)
    # print(id2node)
    print(start)
    print(end)
if __name__ == '__main__':
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
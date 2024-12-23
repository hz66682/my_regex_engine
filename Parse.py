import sys
class Parse:

    def parse_or(r, idx):
        idx, prev = Parse.parse_and(r, idx)
        while idx < len(r):
            if r[idx] == ')':
                break
            idx, node = Parse.parse_and(r, idx + 1)
            prev = ('|', prev, node)
        return idx, prev
    def parse_and(r, idx):
        prev = None
        while idx < len(r):
            if r[idx] in '|)':
                break
            idx, node = Parse.parse_node(r, idx)
            if prev is None:
                prev = node
            else:
                prev = ('&', prev, node)
        return idx, prev
    def parse_node(r, idx):
        ch = r[idx]
        idx += 1
        if ch == '(':
            idx, node = Parse.parse_or(r, idx)
            if idx < len(r) and r[idx] == ')':
                idx += 1
            else:
                raise ValueError("Invalid input")
        elif ch in "*+{":
            raise ValueError("Invalid input")
        else:
            node = ch
        idx, node = Parse.parse_postfix(r, idx, node)
        return idx, node
    def parse_postfix(r, idx, node):
        if idx >= len(r) or r[idx] not in "*+{":
            return idx, node
        ch = r[idx]
        idx += 1
        if ch == '*':
            minn = 0
            maxn = sys.maxsize
        elif ch == '+':
            minn = 1
            maxn = sys.maxsize
        elif ch == '{':
            idx, minn = Parse.parse_int(r, idx)
            while idx < len(r) and r[idx] == ' ':
                idx += 1
            if idx < len(r) and r[idx] == ',':
                idx, maxn = Parse.parse_int(r, idx + 1)
                if maxn is None:
                    maxn = sys.maxsize
            if idx < len(r) and r[idx] == '}':
                idx += 1
            else:
                raise ValueError("Invalid input")
        return idx, ('postfix', node, minn, maxn)
    def parse_int(r, idx):
        pre = idx
        while idx < len(r) and r[idx].isdigit():
            idx += 1
        return idx, int(r[pre:idx]) if pre != idx else 0
    def parse(r):
        idx, node = Parse.parse_or(r, 0)
        if idx != len(r):
            raise ValueError("Invalid input")
        return node
if __name__ == '__main__':
    assert Parse.parse('') is None
    assert Parse.parse('.') == '.'
    assert Parse.parse('a') == 'a'
    assert Parse.parse('ab') == ('&', 'a', 'b')
    assert Parse.parse('a|b') == ('|', 'a', 'b')
    assert Parse.parse('a+') == ('postfix', 'a', 1, sys.maxsize)
    assert Parse.parse('a{3,6}') == ('postfix', 'a', 3, 6)
    assert Parse.parse('a|bc') == ('|', 'a', ('&', 'b', 'c'))
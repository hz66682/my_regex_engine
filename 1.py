class SimpleRegex:
    def __init__(self, pattern):
        self.pattern = pattern
        
    def match(self, text):
        return self._match_helper(self.pattern, text, 0, 0)
    
    def _match_helper(self, pattern, text, pattern_pos, text_pos):
        # 如果模式串和文本都到达末尾,说明匹配成功
        if pattern_pos == len(pattern) and text_pos == len(text):
            return True
            
        # 如果模式串到达末尾但文本没有,或文本到达末尾但模式串没有(且下一个不是*),则匹配失败
        if pattern_pos == len(pattern):
            return False
            
        # 处理 * 的情况
        if pattern_pos + 1 < len(pattern) and pattern[pattern_pos + 1] == '*':
            # 跳过当前字符和*
            if self._match_helper(pattern, text, pattern_pos + 2, text_pos):
                return True
                
            # 尝试匹配当前字符0次或多次
            while (text_pos < len(text) and 
                   (pattern[pattern_pos] == '.' or pattern[pattern_pos] == text[text_pos])):
                if self._match_helper(pattern, text, pattern_pos + 2, text_pos + 1):
                    return True
                text_pos += 1
            return False
            
        # 如果文本到达末尾,匹配失败
        if text_pos == len(text):
            return False
            
        # 匹配单个字符
        if (pattern[pattern_pos] == '.' or pattern[pattern_pos] == text[text_pos]):
            return self._match_helper(pattern, text, pattern_pos + 1, text_pos + 1)
            
        return False

# 使用示例
def test_regex():
    # 测试普通字符匹配
    regex = SimpleRegex("abc")
    assert regex.match("abc") == True
    assert regex.match("abcd") == False
    
    # 测试 . 匹配
    regex = SimpleRegex("a.c")
    assert regex.match("abc") == True
    assert regex.match("acc") == True
    assert regex.match("ac") == False
    
    # 测试 * 匹配
    regex = SimpleRegex("ab*c")
    assert regex.match("ac") == True
    assert regex.match("abc") == True
    assert regex.match("abbc") == True
    assert regex.match("abbbc") == True
    
    print("所有测试用例通过!")

if __name__ == "__main__":
    test_regex()

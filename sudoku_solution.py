from collections import defaultdict, deque


class Solution:
    def solveSudoku(self, board) -> None:
        """
        Do not return anything, modify board in-place instead.
        """
        m, n = len(board), len(board[0])
        
        def compileChoices(board, choices, decision_points):
            rs = [set() for i in range(9)]
            cs = [set() for i in range(9)]
            ss = defaultdict(lambda: set())
            to_decide = 0
            
            for i in range(9):
                for j in range(9):
                    if board[i][j] != 0: 
                        rs[i].add(board[i][j])
                        cs[j].add(board[i][j])
                        
                        si = i // 3
                        sj = j // 3
                        ss[(si, sj)].add(board[i][j])
            for i in range(9):
                for j in range(9):
                    if board[i][j] != 0: continue
                    choices[i][j] = set([x for x in range(1,10)])
                    choices[i][j] -= rs[i]
                    choices[i][j] -= cs[j]
                    choices[i][j] -= ss[(i//3, j//3)]
                    
                    # print(i, j, choices[i][j])
                    if len(choices[i][j]) == 1:
                        decision_points.append((i, j))
                        to_decide += 1
                    elif len(choices[i][j]) > 1:
                        to_decide += 1
                    else:
                        # print(i, j, choices[i][j], "no choice?")
                        return -1                
            return to_decide                  
        
        def updateChoices(board, choices, decision_points, to_decide):
            
            while decision_points:
                r, c = decision_points.pop()
                if len(choices[r][c]) == 0:
                    if board[r][c] == 0: return -1
                    else: continue
                board[r][c] = choices[r][c].pop()
                to_decide -= 1
                if to_decide == 0: return 0
                
                for i in range(9):
                    if i == r: continue
                    if board[i][c] != 0: continue
                    if board[r][c] in choices[i][c]: choices[i][c].remove(board[r][c])
                    if len(choices[i][c]) == 1: 
                        decision_points.append((i, c))
                    elif len(choices[i][c]) == 0:
                        return -1                    
                for j in range(9):
                    if j == c: continue
                    if board[r][j] != 0: continue
                    if board[r][c] in choices[r][j]: choices[r][j].remove(board[r][c])
                    if len(choices[r][j]) == 1:
                        decision_points.append((r, j))
                    elif len(choices[r][j]) == 0:
                        return -1        
                for si in range(3):
                    for sj in range(3):
                        i = r // 3 * 3 + si
                        j = c // 3 * 3 + sj
                        if i == r: continue
                        if j == c: continue
                        if board[i][j] != 0: continue
                        if board[r][c] in choices[i][j]: choices[i][j].remove(board[r][c])
                        if len(choices[i][j]) == 1: 
                            decision_points.append((i, j))
                        elif len(choices[i][j]) == 0:
                            return -1                  
            return to_decide
        
        def copyBoard(bd1, bd2):
            for i in range(m):
                for j in range(n):
                    bd1[i][j] = bd2[i][j]
                    
        def copyChoices(c1, c2):
            for r in range(9):
                for c in range(9):
                    c1[r][c] = c2[r][c].copy()
                    
        def getPos(cs):
            for r in range(9):
                for c in range(9):
                    if len(cs[r][c]): return r, c
        
        choices = [ [set() for i in range(10) ]  for j in range(10)]
        decision_points = []
        to_decide = compileChoices(board, choices, decision_points)

        brd_states = deque([(board, choices, decision_points, to_decide)])
        
        while brd_states:
            
            bd, cs, ds, td = brd_states.popleft()
            
            rv = updateChoices(bd, cs, ds, td)
            if rv == 0:
                print("Succeeded")
                copyBoard(board, bd)
                return
            if rv == -1: 
                continue      

            nxt_td = rv
            r, c = getPos(cs) 
            for choice in cs[r][c]:
                nxt_bd =  [[0]*9 for i in range(9)]
                copyBoard(nxt_bd, bd)
                nxt_cs = nxt_cs = [ [set() for i in range(10) ]  for j in range(10)]
                copyChoices(nxt_cs, cs)
                nxt_cs[r][c] = {choice}
                nxt_ds = [(r, c)]
                brd_states.append((nxt_bd, nxt_cs, nxt_ds, nxt_td))


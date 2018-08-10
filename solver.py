
import chopsticks as game
WIN = "win"
LOSE = "lose"
TIE = "tie"
UNKNOWN = "unknown"
DRAW = "draw"
Cur_game = game
Frontier = []
Tree = {}


def discover(position):
    queue = [position]
    global Frontier, Tree
    while(queue):
        position = queue.pop(0)
        if position in Tree:
            continue
        if Cur_game.primitive(position) != UNKNOWN:
            Tree[position] = [0, Cur_game.primitive(position), 0]
            Frontier.append([position, Cur_game.primitive(position)])
        else:
            children = Cur_game.children(position)
            Tree[position] = [len(children), UNKNOWN, UNKNOWN]
            queue.extend(children)

def solve(position):
    global Tree, Frontier
    if position in Cur_game.VALUES:
        return Cur_game.VALUES[position][1:3]
    else:
        Tree = {}
        Frontier = []
        discover(position)
        #print(Tree)
        while(len(Frontier) != 0):
            cur = Frontier.pop(0)
            parent = Cur_game.parent(cur[0])
            #print(cur, parent)
            if cur[1] == LOSE:
                # current node is lose position, its parents are all win position
                for p in parent:
                    if p in Tree and p not in Cur_game.VALUES:
                        # p not in Tree is illegal or has been found
                        remote = Tree[cur[0]][2] + 1 if (Tree[p][2] == UNKNOWN or Tree[p][2] == TIE) else min(Tree[cur[0]][2] + 1, Tree[p][2])
                        Tree[p] = [0, WIN, remote]
                        Cur_game.VALUES[p] = Tree[p]
                        #print(p, Tree[p])
                        Frontier.append([p, WIN])
            elif cur[1] == TIE:
                for p in parent:
                    if p in Tree and p not in Cur_game.VALUES:
                        remote = Tree[cur[0]][2] + 1
                        if Tree[p][1] == UNKNOWN:
                            Tree[p][1] = TIE
                        Tree[p][0] = Tree[p][0] - 1
                        if Tree[p][0] == 0:
                            Tree[p] = [0, TIE, remote]
                            Cur_game.VALUES[p] = Tree[p]
                            #print(p, Tree[p])
                            Frontier.append([p, TIE])
            elif cur[1] == WIN:
                for p in parent:
                    if p in Tree and p not in Cur_game.VALUES:
                        Tree[p][0] = Tree[p][0] - 1
                        if Tree[p][0] == 0:
                            remote = Tree[cur[0]][2] + 1 if (Tree[p][2] == UNKNOWN) else max(Tree[cur[0]][2] + 1,
                                                                                                Tree[p][2])
                            if Tree[p][1] == TIE:
                                Frontier.append([p, TIE])
                            else:
                                Tree[p] = [0, LOSE, remote]
                                Cur_game.VALUES[p] = Tree[p]
                                #print(p, Tree[p])
                                Frontier.append([p, LOSE])
        #draw condition
        for item in Tree.items():
            if item[1][1] == UNKNOWN:
                item[1][1] = DRAW
        #print(Tree)
    return Tree[position][1:3]

from backend.dataflow.basicblock import BasicBlock

"""
CFG: Control Flow Graph

nodes: sequence of basicblock
edges: sequence of edge(u,v), which represents after block u is executed, block v may be executed
links: links[u][0] represent the Prev of u, links[u][1] represent the Succ of u,
"""


class CFG:
    def __init__(self, nodes: list[BasicBlock], edges: list[(int, int)]) -> None:
        self.nodes = nodes
        self.edges = edges

        self.links = []

        for i in range(len(nodes)):
            self.links.append((set(), set()))

        # represents u -> v
        for (u, v) in edges:
            self.links[u][1].add(v)
            self.links[v][0].add(u)

    def getBlock(self, id):
        return self.nodes[id]

    def getPrev(self, id):
        return self.links[id][0]

    def getSucc(self, id):
        return self.links[id][1]

    def getInDegree(self, id):
        return len(self.links[id][0])

    def getOutDegree(self, id):
        return len(self.links[id][1])

    def iterator(self):
        return iter(self.nodes)

    # * Step 7
    def unreachable(self, id):
        # 通过调用 getPrev 函数进行 DFS 来判断当前 id 的 block 是否可达
        # 如果可达，返回 False，否则返回 True
        
        # 1. 如果当前 id 为 0，说明当前 block 是入口 block，返回 False
        if id == 0:
            return False
        
        # 2. 如果当前 id 的 block 的 inDegree 不为 0，说明当前 block 不是入口 block，进行 DFS
        # 2.1. 初始化一个栈，将当前 id 的 block 的 id 压入栈中
        stack = [id]
        # 2.2. 初始化一个集合，用于存储已经访问过的 block 的 id
        visited = set()
        # 2.3. 当栈不为空时，进行循环
        while stack:
            # 2.3.1. 将栈顶的 block 的 id 出栈
            cur_id = stack.pop()
            
            # 2.3.2. 如果当前 block 的 id 已经访问过，跳过
            if cur_id in visited:
                continue
            # 2.3.3. 将当前 block 的 id 加入到 visited 集合中
            visited.add(cur_id)
            # 2.3.4. 将当前 block 的所有前驱 block 的 id 压入栈中
            for prev_id in self.getPrev(cur_id):
                if prev_id == 0:
                    return False 
                stack.append(prev_id)
            
            
        return True
            
        
import ast
import inspect
import networkx as nx


def fibonacci(n: int):
    a = 0
    b = 1
    for _ in range(n):
        tmp = b
        b = a + b
        a = tmp
    return a


class MyNodeVisitor(ast.NodeVisitor):
    def __init__(self):
        self.graph = nx.DiGraph()

    def visit_Module(self, node):
        self.visit(node.body[0])

    def visit_FunctionDef(self, node):
        self.graph.add_node(str(node), color='black', label=f'fun {node.name}')
        self.visit_children(node)
        return str(node)

    def visit_If(self, node):
        self.graph.add_node(str(node), color='yellow', label='if')
        self.visit_children(node)
        return str(node)

    def visit_Return(self, node):
        self.graph.add_node(str(node), color='red', label=f'return')
        self.graph.add_edge(str(node), self.visit(node.value))
        return str(node)

    def visit_Constant(self, node):
        self.graph.add_node(str(node), label=f'const {node.value}', color="teal")
        return str(node)

    def visit_Assign(self, node):
        self.graph.add_node(str(node), label='assign', color="aqua")
        for target in node.targets:
            self.graph.add_edge(str(node), self.visit(target), label='target')
        self.graph.add_edge(str(node), self.visit(node.value), label='value')
        return str(node)

    def visit_Subscript(self, node):
        self.graph.add_node(str(node), label='subscript', color="green")
        self.graph.add_edge(str(node), self.visit(node.slice), label='slice')
        self.graph.add_edge(str(node), self.visit(node.value), label='value')
        return str(node)

    def visit_Name(self, node):
        self.graph.add_node(str(node), label=f'name {node.id}', color='lime')
        return str(node)

    def visit_BinOp(self, node):
        self.graph.add_node(str(node), label=f'binOp {node.op.__class__.__name__}', color='blue')
        self.graph.add_edge(str(node), self.visit(node.left), label='left')
        self.graph.add_edge(str(node), self.visit(node.right), label='right')
        return str(node)

    def visit_Call(self, node):
        self.graph.add_node(str(node), label='Call', color='purple')
        for arg in node.args:
            self.graph.add_edge(node, self.visit(arg), label='arg')
        self.graph.add_edge(node, self.visit(node.func), label='func')
        return str(node)

    def visit_For(self, node):
        self.graph.add_node(str(node), label='For', color='brown')

        self.graph.add_edge(str(node), self.visit(node.iter), label='iter')
        self.graph.add_edge(str(node), self.visit(node.target), label='target')
        for b in node.body:
            self.graph.add_edge(str(node), self.visit(b), label='body')
        return str(node)

    def visit_children(self, node):
        for child in node.body:
            self.graph.add_edge(node, self.visit(child))

    def generic_visit(self, node):
        return


if __name__ == "__main__":
    tree = ast.parse(inspect.getsource(fibonacci))
    v = MyNodeVisitor()
    v.visit(tree)
    G = v.graph
    p = nx.drawing.nx_pydot.to_pydot(G)
    p.write_png('artifacts/result.png')
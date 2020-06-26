class Interpreter:
    def __init__(self):
        pass

    def process_node(self, node):
        node_name = f'visit_{type(node).__name__}' # get name of the passed node
        method = getattr(self, node_name, self.no_found_fun)

        return method(node)

    def no_found_fun(self, node):
        raise Exception("No visit method defined")

    def visit_NumberNode(self, node):
        print("Found num node")

    def visit_OperatorNode(self, node):
        print("found op node")
        self.process_node(node.left_node)
        self.process_node(node.right_node)

    def visit_UnaryNode(self, node):
        print("found un node")
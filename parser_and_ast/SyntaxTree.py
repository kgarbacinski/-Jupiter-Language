class NumberNode:
    def __init__(self, _value):
        self.token = _value

    def __repr__(self):
        return f'{self.token}'

class OperatorNode:
    def __init__(self, _left_node, _op_token, _right_node):
        self.left_node = _left_node
        self.right_node = _right_node
        self.op_token = _op_token

    def __repr__(self):
        return f'({self.left_node}, {self.op_token}, {self.right_node})'
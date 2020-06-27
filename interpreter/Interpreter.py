from lexer.Tokens import *
from interpreter.IntResult import *
from error.Error import *


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
        return IntResult().success(Number(node.token.value))

    def visit_OperatorNode(self, node):
        result = IntResult()

        left = result.register(self.process_node(node.left_node))
        if result.error: return result
        right = result.register(self.process_node(node.right_node))
        if result.error: return result

        if node.op_token.type == T_PLUS:
            number, error = left.addition(right)
        elif node.op_token.type == T_MINUS:
            number, error = left.substracting(right)
        elif node.op_token.type == T_MUL:
            number, error = left.multiplying(right)
        elif node.op_token.type == T_DIV:
            mnumber, error = left.division(right)

        if error:
            return result.failure(error)
        else:
            return result.success(number)

    def visit_UnaryNode(self, node):
        result = IntResult()

        number = result.register(self.process_node(node.node))
        if result.error: return result

        error = None
        if node.op_token.type == T_MINUS:
            number, error = number.multiplying(Number(-1))

        if error:
            return result.failure(error)
        else:
            return result.success(number)



#################
# Number Storage
#################

class Number:
    def __init__(self, value_):
        self.value = value_

    def addition(self, other_num):
        if isinstance(other_num, Number):
            return Number(self.value + other_num.value), None

    def substracting(self, other_num):
        if isinstance(other_num, Number):
            return Number(self.value - other_num.value), None

    def multiplying(self, other_num):
        if isinstance(other_num, Number):
            return Number(self.value * other_num.value), None

    def division(self, other_num):
        if isinstance(other_num, Number):
            if other_num.value == 0:
                return None, InterpreterError("Division by zero")

            return Number(self.value / other_num.value), None

    def __repr__(self):
        return str(self.value)
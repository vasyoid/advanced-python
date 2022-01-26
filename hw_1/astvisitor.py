import ast


BLUE = "#9999EE"
GREEN = "#99EE99"
YELLOW = "#EEEE99"
CYAN = "#99EEEE"
PINK = "#EE9999"


class NxVisitor(ast.NodeVisitor):
    def __init__(self):
        self._node_id = 0
        self._stack = []
        self._cur_edge = None
        self.root = None
        self.labels = {}
        self.colors = {}
        self.edge_labels = {}

    def my_visit(self, ast_node, label, color=BLUE, visit_children=None):
        node = {"id": self._node_id, "children": []}
        self._node_id += 1

        if self._stack and self._cur_edge is not None:
            self.edge_labels[(self._stack[-1]["id"], node["id"])] = self._cur_edge
            self._cur_edge = None

        self._stack.append(node)
        if visit_children is None:
            super(self.__class__, self).generic_visit(ast_node)
        else:
            visit_children()
        self._stack.pop()
        self.labels[node["id"]] = label
        self.colors[node["id"]] = color
        if self._stack:
            self._stack[-1]["children"].append(node)
        else:
            self.root = node

    def generic_visit(self, node):
        self.my_visit(node, type(node))

    def visit_Module(self, node):
        super(self.__class__, self).generic_visit(node)

    def visit_FunctionDef(self, node):
        self.my_visit(node, f"function\n{node.name}")

    def visit_arguments(self, node):
        self.my_visit(node, "arguments")

    def visit_arg(self, node):
        self.my_visit(node, f"argument\n{node.arg}", color=GREEN)

    def visit_If(self, node):
        def _visit_children():
            self._cur_edge = "condition"
            self.visit(node.test)
            for body in node.body:
                self._cur_edge = "if-body"
                self.visit(body)
            for orelse in node.orelse:
                self._cur_edge = "else-body"
                self.visit(orelse)

        self.my_visit(node, "if", visit_children=_visit_children)

    def visit_Compare(self, node):
        self.my_visit(node, "compare", color=CYAN)

    def visit_Lt(self, node):
        self.my_visit(node, "<", color=CYAN)

    def visit_Load(self, node):
        pass

    def visit_Name(self, node):
        self.my_visit(node, f"variable\n{node.id}", color=GREEN)

    def visit_Constant(self, node):
        self.my_visit(node, f"constant\n{node.value}", color=YELLOW)

    def visit_Return(self, node):
        self.my_visit(node, "return")

    def visit_BinOp(self, node):
        self.my_visit(node, "binary\noperation", color=CYAN)

    def visit_Add(self, node):
        self.my_visit(node, "+", color=CYAN)

    def visit_Sub(self, node):
        self.my_visit(node, "-", color=CYAN)

    def visit_Call(self, node):
        def _visit_children():
            for arg in node.args:
                self.visit(arg)
            for keyword in node.keywords:
                self.visit(keyword)

        self.my_visit(node, f"call\n{getattr(node.func, 'id')}", visit_children=_visit_children, color=PINK)

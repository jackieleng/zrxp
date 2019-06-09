from parsimonious import Grammar, NodeVisitor


# TODO: comments
grammar = Grammar(
    r"""
    zrxp = single_timeseries+
    single_timeseries = metadata_headers records

    metadata_headers = metadata_header+
    records = record+

    metadata_header = hashtag (metadata_field metadata_sep)+ ws
    hashtag = "#"
    metadata_field = ~r"[-\w\.\(\)\,\-\s]+"
    metadata_sep = "|*|"

    record = field (field_sep field)* ws
    field = ~r"[-\w\d\.]+"
    field_sep = ~r"[ \t]+"

    comment = ~r"##.*"
    newline = ~r"[\n\r]+"
    ws = ~r"\s*"
    """
)


class ZRXPVisitor(NodeVisitor):
    def visit_zrxp(self, node, visited_children):
        return visited_children

    def visit_single_timeseries(self, node, visited_children):
        metadata, records = visited_children
        output = {"metadata": metadata, "records": records}
        return output

    def visit_metadata_headers(self, node, visited_children):
        flat_list = [item for sublist in visited_children for item in sublist]
        return flat_list

    def visit_metadata_header(self, node, visited_children):
        _, metadata, _ = visited_children
        return [field for (field, sep) in metadata]

    def visit_metadata_field(self, node, visited_children):
        return node.text

    def visit_records(self, node, visited_children):
        return visited_children

    def visit_record(self, node, visited_children):
        field, fields_comb, _ = visited_children
        fields = [f for _, f in fields_comb]
        return [field] + fields

    def visit_field(self, node, visited_children):
        return node.text

    def generic_visit(self, node, visited_children):
        return visited_children or node


zv = ZRXPVisitor()
with open("05BJ004.HG.datum.O.zrx", "r") as f:
    s = f.read()
    tree = grammar.parse(s)
    print(tree)

    output = zv.visit(tree)
    print(output)

zv = ZRXPVisitor()
with open("multi_ts.zrx", "r") as f:
    s = f.read()
    tree_multi = grammar.parse(s)
    print(tree_multi)

    output_multi = zv.visit(tree_multi)
    print(output_multi)

from io import StringIO
from pathlib import Path

import pandas as pd
from parsimonious import Grammar, NodeVisitor


# TODO: comments
ZRXP_GRAMMAR = Grammar(
    r"""
    zrxp = single_timeseries+
    single_timeseries = metadata_headers records

    metadata_headers = metadata_header+
    records = record+

    metadata_header = hashtag (metadata_field metadata_sep+)+ ws
    hashtag = "#"
    metadata_field = metadata_key? metadata_value
    metadata_key =
        "ZRXPVERSION" / "ZRXPMODE" / "SANR" / "REXCHANGE" / "TZ" /
        "SNAME" / "CNR" / "RTIMEVL" / "CUNIT" / "RINVAL" /
        "RNR" / "LAYOUT"
    metadata_value = ~r"((?!(\|\*\|)).)+"
    metadata_sep = "|*|"

    record = field (field_sep field)* ws
    field = ~r"[-\w\d\.]+"
    field_sep = ~r"[ \t]+"

    comment = ~r"##.*"
    newline = ~r"[\n\r]+"
    ws = ~r"\s*"
    """
)


# zrxp grammer without explicit parsing of record fields
# i.e., this can be done using a more efficient parser like
# pandas.read_csv
ZRXP_GRAMMAR_SIMPLE = Grammar(
    r"""
    zrxp = single_timeseries+
    single_timeseries = metadata_headers records

    metadata_headers = metadata_header+
    records = !hashtag ~r"[\w\d\s\.,-]*"

    metadata_header = hashtag (metadata_field metadata_sep+)+ ws
    metadata_field = metadata_key? metadata_value
    metadata_key =
        "ZRXPVERSION" / "ZRXPMODE" / "SANR" / "REXCHANGE" / "TZ" /
        "SNAME" / "CNR" / "RTIMEVL" / "CUNIT" / "RINVAL" /
        "RNR" / "LAYOUT"
    metadata_value = ~r"((?!(\|\*\|)).)+"
    metadata_sep = "|*|"


    hashtag = "#"
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
        k, v = visited_children
        try:
            return (k[0], v)
        except TypeError:
            return (k.text, v)

    def visit_metadata_key(self, node, visited_children):
        return node.text

    def visit_metadata_value(self, node, visited_children):
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


class SimpleZRXPVisitor(NodeVisitor):
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
        k, v = visited_children
        try:
            return (k[0], v)
        except TypeError:
            return (k.text, v)

    def visit_metadata_key(self, node, visited_children):
        return node.text

    def visit_metadata_value(self, node, visited_children):
        return node.text

    def visit_records(self, node, visited_children):
        return node

    # def visit_record(self, node, visited_children):
    #     field, fields_comb, _ = visited_children
    #     fields = [f for _, f in fields_comb]
    #     return [field] + fields

    # def visit_field(self, node, visited_children):
    #     return node.text

    def generic_visit(self, node, visited_children):
        return visited_children or node


zrxp_visitor = ZRXPVisitor()
simple_zrxp_visitor = SimpleZRXPVisitor()


def parse(s: str):
    """
    Parse zrxp file and split the metadata according to zrxp keywords.
    """
    tree = ZRXP_GRAMMAR.parse(s)
    return zrxp_visitor.visit(tree)


def parse_pandas(s: str):
    """
    Parse zrxp string and use pandas for parsing records.
    """
    tree = ZRXP_GRAMMAR_SIMPLE.parse(s)
    result = simple_zrxp_visitor.visit(tree)
    for ts in result:
        ts["records"] = pd.read_csv(StringIO(ts["records"].text))
    return result


def parse_file(filepath: str, engine: str = "default"):
    """
    Open and parse a zrxp file.
    """
    path = Path(filepath)
    text = path.read_text()
    engines = {"default": parse, "pandas": parse_pandas}
    return engines[engine](text)


output = parse_file("data/05BJ004.HG.datum.O.zrx", engine="pandas")
print(output)
# output2 = parse_file("data/K-Greim-SG-cmd-2000-2004.zrx", engine='pandas')
# print(output2)
output_multi = parse_file("data/multi_ts.zrx", engine="pandas")
print(output_multi)

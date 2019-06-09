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
        "ZRXPVERSION" / "ZRXPMODE" / "ZRXPCREATOR" /
        "SANR" / "SNAME" /
        "REXCHANGE" / "TZ" /
        "CNR" / "CNAME" / "CTYPE" / "CUNIT" /
        "RTIMELVL" / "RINVAL" / "RNR" /
        "LAYOUT" / "TSPATH"
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
        "ZRXPVERSION" / "ZRXPMODE" / "ZRXPCREATOR" /
        "SANR" / "SNAME" /
        "REXCHANGE" / "TZ" /
        "CNR" / "CNAME" / "CTYPE" / "CUNIT" /
        "RTIMELVL" / "RINVAL" / "RNR" /
        "LAYOUT" / "TSPATH"
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

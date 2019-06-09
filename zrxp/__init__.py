from io import StringIO
from pathlib import Path

import pandas as pd

from .grammar import (
    ZRXP_GRAMMAR, ZRXP_GRAMMAR_SIMPLE, ZRXPVisitor, SimpleZRXPVisitor
)

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


# output = parse_file("data/05BJ004.HG.datum.O.zrx", engine="pandas")
# print(output)
# output2 = parse_file("data/K-Greim-SG-cmd-2000-2004.zrx", engine='pandas')
# print(output2)
# output_multi = parse_file("data/multi_ts.zrx", engine="pandas")
# print(output_multi)

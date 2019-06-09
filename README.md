# zrxp

ZRXP parser. Uses `parsimonious` for generic grammar definition and parsing,
and (optionally) `pandas` for parsing the time series data block with
increased performance.


```
>>> import zrxp
>>> ts_list = zrxp.parse_file('./data/K-Greim-SG-cmd-2000-2004.zrx', engine='pandas')
>>> ts = ts_list[0]
>>> ts['metadata']
[('TZ', 'UTC+1'),
 ('CTYPE', 'n-min-ip'),
 ('CUNIT', 'M'),
 ('RINVAL', '-777'),
 ('RNR', '-1')]
>>> ts['records'].head()
0  20000101000000 2.26   127 3
1  20000101001500 2.26   127 3
2  20000101003000 2.26   127 3
3  20000101004500 2.26   127 3
4  20000101010000 2.26   127 3
```

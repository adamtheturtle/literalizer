from collections import OrderedDict
my_data = OrderedDict([
    ("""\
  leading
key  """, """\
  leading
value
  """),
    ("""\
next
\tkey""", ("""\

first
""", """\
 last
 """)),
])

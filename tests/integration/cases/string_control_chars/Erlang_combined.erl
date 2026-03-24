-module(check).
-export([my_data/0]).
my_data() ->
    My_data = [
    "line1\r\nline2",
    "line1\rline2",
    ""
],
    My_data.

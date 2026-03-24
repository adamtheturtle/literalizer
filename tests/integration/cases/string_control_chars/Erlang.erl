-module(check).
-export([x/0]).
x() ->
    My_data = [
    "line1\r\nline2",
    "line1\rline2",
    ""
],
    My_data.

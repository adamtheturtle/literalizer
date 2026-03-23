-module(check).
-export([x/0]).
x() ->
    [
    "line1\r\nline2",
    "line1\rline2",
    ""
].

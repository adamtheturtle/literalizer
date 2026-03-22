-module(check).
-export([x/0]).
x() ->
    My_data = [
    "C:\\path\\to\\file",
    "back\\\\slash",
    "hello \\\"world\\\""
],
    My_data.

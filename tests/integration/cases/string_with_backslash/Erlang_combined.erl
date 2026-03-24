-module(check).
-export([my_data/0]).
my_data() ->
    My_data = [
    "C:\\path\\to\\file",
    "back\\\\slash",
    "hello \\\"world\\\""
],
    My_data.

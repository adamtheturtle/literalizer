-module(check).
-export([my_data/0]).
my_data() ->
    [
    42,
    3.14,
    true,
    false,
    "hello \"world\""
].

-module(fixture_rust_lazy_static_empty_sibling_erlang).
-export([x/0]).
x() ->
    My_data = #{
        "a" => [[1, 2], [3]],
        "b" => [[], [1]]
    },
    My_data.

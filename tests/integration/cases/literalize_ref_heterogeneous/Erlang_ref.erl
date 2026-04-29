-module(fixture_literalize_ref_heterogeneous_erlang_ref).
-export([x/0]).
x() ->
    My_data = #{
        "a" => 1,
        "b" => "hello"
    },
    My_data.

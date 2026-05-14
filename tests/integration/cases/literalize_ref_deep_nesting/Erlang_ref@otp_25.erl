-module(fixture_literalize_ref_deep_nesting_erlang_ref).
-export([x/0]).
x() ->
    Deep = #{
        "_" => "_"
    },
    My_data = #{
        "a" => #{"b" => #{"c" => Deep}}
    },
    My_data.

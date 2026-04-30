-module(fixture_literalize_ref_deep_nesting_erlang).
-export([x/0]).
x() ->
    My_data = #{
        "a" => #{"b" => #{"c" => #{"$ref" => "deep"}}}
    },
    My_data.

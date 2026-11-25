-module(fixture_literalize_ref_default_nested_erlang_ref_default).
-export([x/0]).
x() ->
    Item_var = #{
        "_" => "_"
    },
    My_data = #{
        "items" => [Item_var, #{"fallback" => "value"}]
    },
    My_data.

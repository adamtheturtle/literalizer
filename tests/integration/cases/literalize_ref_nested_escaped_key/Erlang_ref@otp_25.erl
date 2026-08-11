-module(fixture_literalize_ref_nested_escaped_key_erlang_ref).
-export([x/0]).
x() ->
    Foo = #{
        "_" => "_"
    },
    My_data = #{
        "items" => [#{"other" => 1}, Foo],
        "mapping" => #{"value" => Foo}
    },
    My_data.

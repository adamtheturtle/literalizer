-module(fixture_consumer_key_binding_erlang_type_hints_safe).
-export([x/0]).
x() ->
    Key_binding = #{
        "a" => 1
    },
    Key_binding.

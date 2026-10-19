-module(fixture_consumer_key_binding_erlang_type_hints_safe).
-export([x/0]).
x() ->
    K = #{
        "a" => 1
    },
    K.

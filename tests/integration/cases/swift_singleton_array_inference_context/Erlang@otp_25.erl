-module(fixture_swift_singleton_array_inference_context_erlang).
-export([x/0]).
x() ->
    My_data = #{
        "nil" => [[[[[[[[[undefined]]]]]]]]],
        "empty" => [[[[[[[[[[]]]]]]]]]],
        "siblings" => [[[[[[[[[[4, 5]]]]]]]]]]
    },
    My_data.

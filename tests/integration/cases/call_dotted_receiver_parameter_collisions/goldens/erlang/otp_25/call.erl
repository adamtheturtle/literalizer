-module(fixture_call_dotted_receiver_parameter_collisions_erlang_call).
-export([x/0]).
'api.worker.process'(_, _) -> ok.
x() ->
    'api.worker.process'(#{}, #{}).

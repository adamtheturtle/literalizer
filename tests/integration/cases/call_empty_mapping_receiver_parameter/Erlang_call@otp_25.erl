-module(fixture_call_empty_mapping_receiver_parameter_erlang_call).
-export([x/0]).
'api.process'(_) -> ok.
x() ->
    'api.process'(#{}).

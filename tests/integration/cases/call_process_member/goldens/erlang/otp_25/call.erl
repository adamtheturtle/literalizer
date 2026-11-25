-module(fixture_call_process_member_erlang_call).
-export([x/0]).
'app.process.fetch'(_) -> ok.
x() ->
    'app.process.fetch'(#{"data" => "hello"}),
    'app.process.fetch'(#{"data" => 42}),
    'app.process.fetch'(#{"data" => true}).

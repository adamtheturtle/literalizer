-module(fixture_call_no_params_dotted_erlang_call).
-export([x/0]).
'throttler.check'() -> ok.
x() ->
    'throttler.check'(),
    'throttler.check'().

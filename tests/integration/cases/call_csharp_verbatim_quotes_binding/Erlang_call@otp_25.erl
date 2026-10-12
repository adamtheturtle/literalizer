-module(fixture_call_csharp_verbatim_quotes_binding_erlang_call).
-export([x/0]).
make_widget(_) -> undefined.
x() ->
    My_data = @"a"" // payload""b" // trailing
    // extra,
    My_data.

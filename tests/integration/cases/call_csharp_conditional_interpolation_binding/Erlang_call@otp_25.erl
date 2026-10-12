-module(fixture_call_csharp_conditional_interpolation_binding_erlang_call).
-export([x/0]).
make_widget(_) -> undefined.
x() ->
    My_data = $"{(true ? "// payload" : "ok")}" // trailing
    // extra,
    My_data.

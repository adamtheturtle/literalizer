-module(fixture_call_csharp_nested_interpolation_binding_erlang_call).
-export([x/0]).
make_widget(_) -> undefined.
x() ->
    My_data = $"{$"{1://}"}" // trailing
    // extra,
    My_data.

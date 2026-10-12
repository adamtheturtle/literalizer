-module(fixture_call_haxe_nested_interpolation_binding_erlang_call).
-export([x/0]).
make_widget(_) -> undefined.
x() ->
    My_data = 'prefix ${'// payload'}' // trailing
    // extra,
    My_data.

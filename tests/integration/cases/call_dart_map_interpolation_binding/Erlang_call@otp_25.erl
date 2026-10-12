-module(fixture_call_dart_map_interpolation_binding_erlang_call).
-export([x/0]).
make_widget(_) -> undefined.
x() ->
    My_data = "${{'value': '// payload'}['value']}" // trailing
    // extra,
    My_data.

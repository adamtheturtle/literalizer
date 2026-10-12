-module(fixture_call_shared_comments_dart_interpolation_comments_new_erlang_call).
-export([x/0]).
make_widget(_) -> undefined.
x() ->
    My_data = ("${ /* } " block */ 42 // } " line
    }").length >= 0 ? make_widget(42) : make_widget(42) // trailing
    // extra,
    My_data.

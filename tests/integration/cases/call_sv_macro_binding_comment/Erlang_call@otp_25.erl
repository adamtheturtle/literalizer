-module(fixture_call_sv_macro_binding_comment_erlang_call).
-export([x/0]).
make_widget(_) -> undefined.
x() ->
    My_data = (`__LINE__ > 0) ? make_widget(42) : make_widget(42) // trailing `marker,
    My_data.

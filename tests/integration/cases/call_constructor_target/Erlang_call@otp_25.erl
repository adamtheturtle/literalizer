-module(fixture_call_constructor_target_erlang_call).
-export([x/0]).
'Playlist.new'(_) -> ok.
x() ->
    'Playlist.new'(1).

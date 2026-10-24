-module(fixture_call_elixir_alias_call_root_erlang_call).
-export([x/0]).
'Playlist.new'(_) -> ok.
x() ->
    'Playlist.new'(1),
    'Playlist.new'(2).

-module(fixture_call_scala_keyword_prefix_member_erlang_call).
-export([x/0]).
'Playlist.newValue'(_) -> ok.
x() ->
    'Playlist.newValue'(1).

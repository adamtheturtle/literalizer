-module(fixture_constructor_binding_erlang_constructor_call).
-export([x/0]).
'Playlist'() -> undefined.
x() ->
    Created = 'Playlist'(),
    Created.

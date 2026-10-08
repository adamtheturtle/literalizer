module [main]

Playlist_new : a -> {}
Playlist_new = \_ -> {}

main =
    dbg (Playlist_new (RInt 1i128))
    {}

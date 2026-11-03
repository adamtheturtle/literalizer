module [main]

Val : [
    RInt I128,
    RList (List Val),
]

main =
    created = Playlist (RInt 1i128)
    expect created == Playlist (RInt 1)
    {}

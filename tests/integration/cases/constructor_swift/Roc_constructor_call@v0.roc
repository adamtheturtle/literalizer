struct Playlist { let value = 42 }

Val : [
    RList (List Val),
]
p = Playlist
precondition(p.value == 42)

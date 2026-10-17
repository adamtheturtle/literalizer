struct Playlist { let value = 42 }

data Val
    = PList (Array Val)
p = Playlist
precondition(p.value == 42)

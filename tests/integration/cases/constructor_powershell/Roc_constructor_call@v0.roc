function Playlist { return 42 }

Val : [
    RList (List Val),
]
p = Playlist
if ($p -ne 42) { throw "Expected constructor result" }

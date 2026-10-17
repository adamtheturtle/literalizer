function Playlist { return 42 }

data Val
    = PList (Array Val)
p = Playlist
if ($p -ne 42) { throw "Expected constructor result" }

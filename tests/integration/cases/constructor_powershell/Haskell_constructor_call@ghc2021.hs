function Playlist { return 42 }

data Val = HList [Val]
p = Playlist
if ($p -ne 42) { throw "Expected constructor result" }

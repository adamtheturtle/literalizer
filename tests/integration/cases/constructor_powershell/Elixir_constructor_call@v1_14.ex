function Playlist { return 42 }

p = Playlist.new()
if ($p -ne 42) { throw "Expected constructor result" }

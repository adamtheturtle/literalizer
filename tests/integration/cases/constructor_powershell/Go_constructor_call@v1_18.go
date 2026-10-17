function Playlist { return 42 }

p := NewPlaylist()
if ($p -ne 42) { throw "Expected constructor result" }

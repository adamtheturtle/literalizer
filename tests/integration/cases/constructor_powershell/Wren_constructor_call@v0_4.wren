function Playlist { return 42 }

var p = Playlist.new()
if ($p -ne 42) { throw "Expected constructor result" }

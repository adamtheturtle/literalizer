function Playlist { return 42 }

var p = new Playlist();
if ($p -ne 42) { throw "Expected constructor result" }

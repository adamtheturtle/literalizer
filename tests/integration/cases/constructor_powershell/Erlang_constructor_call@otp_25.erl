function Playlist { return 42 }

P = 'Playlist'(),
if ($p -ne 42) { throw "Expected constructor result" }

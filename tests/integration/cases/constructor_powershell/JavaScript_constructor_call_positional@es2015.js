function Playlist { return 42 }

const p = new Playlist();
if ($p -ne 42) { throw "Expected constructor result" }

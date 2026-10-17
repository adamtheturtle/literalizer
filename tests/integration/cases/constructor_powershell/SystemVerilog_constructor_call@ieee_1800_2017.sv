function Playlist { return 42 }

static _VVal p = Playlist();
if ($p -ne 42) { throw "Expected constructor result" }

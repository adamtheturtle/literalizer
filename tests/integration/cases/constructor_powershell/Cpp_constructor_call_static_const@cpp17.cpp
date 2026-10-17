function Playlist { return 42 }

static const auto p = Playlist();
if ($p -ne 42) { throw "Expected constructor result" }

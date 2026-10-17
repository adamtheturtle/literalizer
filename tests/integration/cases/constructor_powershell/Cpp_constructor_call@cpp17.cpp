function Playlist { return 42 }

auto p = Playlist();
if ($p -ne 42) { throw "Expected constructor result" }

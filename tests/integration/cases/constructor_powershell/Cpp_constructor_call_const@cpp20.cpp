function Playlist { return 42 }

const auto p = Playlist();
if ($p -ne 42) { throw "Expected constructor result" }

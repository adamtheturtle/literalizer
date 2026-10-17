function Playlist { return 42 }

declare p="$(Playlist)"
if ($p -ne 42) { throw "Expected constructor result" }

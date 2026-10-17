function Playlist { return 42 }

let p = Playlist::new();
if ($p -ne 42) { throw "Expected constructor result" }

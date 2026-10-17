function Playlist { return 42 }

p : A_Val := Playlist;
if ($p -ne 42) { throw "Expected constructor result" }

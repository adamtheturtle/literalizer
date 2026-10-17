function Playlist { return 42 }

Dim p = New Playlist()
if ($p -ne 42) { throw "Expected constructor result" }

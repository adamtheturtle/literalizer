function Playlist { return 42 }

type Val =
    | FList of Val list
let p = Playlist
if ($p -ne 42) { throw "Expected constructor result" }

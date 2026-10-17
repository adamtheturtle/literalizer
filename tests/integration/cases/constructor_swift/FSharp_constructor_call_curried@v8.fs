struct Playlist { let value = 42 }

type Val =
    | FList of Val list
let p = Playlist
precondition(p.value == 42)

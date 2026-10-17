class Playlist {}

type Val =
    | FList of Val list
let p = Playlist
assert p instanceof Playlist

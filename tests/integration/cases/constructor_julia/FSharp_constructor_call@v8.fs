struct Playlist end

type Val =
    | FList of Val list
let p = Playlist()
@assert p isa Playlist

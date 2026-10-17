class Playlist:
    pass


type Val =
    | FList of Val list
let p = Playlist()
assert isinstance(p, Playlist)

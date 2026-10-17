class Playlist {
    constructor(_options = {}) {}
}

type Val =
    | FList of Val list
let p = Playlist
if (!(p instanceof Playlist)) {
    throw new Error("Expected a Playlist instance");
}

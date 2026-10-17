class Playlist {
    constructor(_options: object = {}) {}
}

type Val =
    | FList of Val list
let p = Playlist
if (!(p instanceof Playlist)) {
    throw new Error("Expected a Playlist instance");
}

export {};

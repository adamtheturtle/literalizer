class Playlist {
    constructor(_options = {}) {}
}

let p = Playlist()
if (!(p instanceof Playlist)) {
    throw new Error("Expected a Playlist instance");
}

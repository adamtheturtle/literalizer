class Playlist {
    constructor(_options = {}) {}
}

let p = Playlist::new();
if (!(p instanceof Playlist)) {
    throw new Error("Expected a Playlist instance");
}

class Playlist {
    constructor(_options = {}) {}
}

p := NewPlaylist()
if (!(p instanceof Playlist)) {
    throw new Error("Expected a Playlist instance");
}

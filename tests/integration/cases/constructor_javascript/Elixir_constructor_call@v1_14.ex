class Playlist {
    constructor(_options = {}) {}
}

p = Playlist.new()
if (!(p instanceof Playlist)) {
    throw new Error("Expected a Playlist instance");
}

class Playlist {
    constructor(_options = {}) {}
}

readonly object? p = new Playlist();
if (!(p instanceof Playlist)) {
    throw new Error("Expected a Playlist instance");
}

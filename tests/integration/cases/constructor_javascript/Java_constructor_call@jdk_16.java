class Playlist {
    constructor(_options = {}) {}
}

var p = new Playlist();
if (!(p instanceof Playlist)) {
    throw new Error("Expected a Playlist instance");
}

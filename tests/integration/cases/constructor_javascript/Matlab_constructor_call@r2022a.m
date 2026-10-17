class Playlist {
    constructor(_options = {}) {}
}

p = Playlist();
if (!(p instanceof Playlist)) {
    throw new Error("Expected a Playlist instance");
}

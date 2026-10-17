class Playlist {
    constructor(_options = {}) {}
}

id p = Playlist();
if (!(p instanceof Playlist)) {
    throw new Error("Expected a Playlist instance");
}

class Playlist {
    constructor(_options = {}) {}
}

CVal p = Playlist();
if (!(p instanceof Playlist)) {
    throw new Error("Expected a Playlist instance");
}

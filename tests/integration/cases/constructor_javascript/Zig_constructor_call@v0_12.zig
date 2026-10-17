class Playlist {
    constructor(_options = {}) {}
}

const p = Playlist();
if (!(p instanceof Playlist)) {
    throw new Error("Expected a Playlist instance");
}

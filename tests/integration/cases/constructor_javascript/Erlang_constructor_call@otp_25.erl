class Playlist {
    constructor(_options = {}) {}
}

P = 'Playlist'(),
if (!(p instanceof Playlist)) {
    throw new Error("Expected a Playlist instance");
}

class Playlist {
    constructor(_options = {}) {}
}

set p [Playlist]
if (!(p instanceof Playlist)) {
    throw new Error("Expected a Playlist instance");
}

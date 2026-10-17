class Playlist {
    constructor(_options: object = {}) {}
}

p := NewPlaylist()
if (!(p instanceof Playlist)) {
    throw new Error("Expected a Playlist instance");
}

export {};

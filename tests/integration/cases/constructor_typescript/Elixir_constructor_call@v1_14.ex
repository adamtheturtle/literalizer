class Playlist {
    constructor(_options: object = {}) {}
}

p = Playlist.new()
if (!(p instanceof Playlist)) {
    throw new Error("Expected a Playlist instance");
}

export {};

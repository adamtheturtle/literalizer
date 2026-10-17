class Playlist {
    constructor(_options: object = {}) {}
}

readonly object? p = new Playlist();
if (!(p instanceof Playlist)) {
    throw new Error("Expected a Playlist instance");
}

export {};

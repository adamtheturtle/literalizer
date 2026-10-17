class Playlist {
    constructor(_options: object = {}) {}
}

static object? p = new Playlist();
if (!(p instanceof Playlist)) {
    throw new Error("Expected a Playlist instance");
}

export {};

class Playlist {
    constructor(_options: object = {}) {}
}

static auto p = Playlist();
if (!(p instanceof Playlist)) {
    throw new Error("Expected a Playlist instance");
}

export {};

class Playlist {
    constructor(_options: object = {}) {}
}

const auto p = Playlist();
if (!(p instanceof Playlist)) {
    throw new Error("Expected a Playlist instance");
}

export {};

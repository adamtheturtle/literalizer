class Playlist {
    constructor(_options: object = {}) {}
}

final Object p = new Playlist();
if (!(p instanceof Playlist)) {
    throw new Error("Expected a Playlist instance");
}

export {};

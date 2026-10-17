class Playlist {
    constructor(_options: object = {}) {}
}

val p = Playlist()
if (!(p instanceof Playlist)) {
    throw new Error("Expected a Playlist instance");
}

export {};

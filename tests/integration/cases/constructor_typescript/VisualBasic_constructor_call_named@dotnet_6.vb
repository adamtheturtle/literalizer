class Playlist {
    constructor(_options: object = {}) {}
}

Dim p = New Playlist()
if (!(p instanceof Playlist)) {
    throw new Error("Expected a Playlist instance");
}

export {};

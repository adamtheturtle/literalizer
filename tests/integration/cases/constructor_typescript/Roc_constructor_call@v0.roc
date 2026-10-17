class Playlist {
    constructor(_options: object = {}) {}
}

Val : [
    RList (List Val),
]
p = Playlist
if (!(p instanceof Playlist)) {
    throw new Error("Expected a Playlist instance");
}

export {};

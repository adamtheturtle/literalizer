class Playlist {
    constructor(_options: object = {}) {}
}

let p = Playlist::new();
if (!(p instanceof Playlist)) {
    throw new Error("Expected a Playlist instance");
}

export {};

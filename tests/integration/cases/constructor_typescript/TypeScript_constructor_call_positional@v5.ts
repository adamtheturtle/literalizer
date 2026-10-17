class Playlist {
    constructor(_options: object = {}) {}
}

const p = new Playlist();
if (!(p instanceof Playlist)) {
    throw new Error("Expected a Playlist instance");
}

export {};

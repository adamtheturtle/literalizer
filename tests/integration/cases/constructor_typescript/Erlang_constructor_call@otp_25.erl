class Playlist {
    constructor(_options: object = {}) {}
}

P = 'Playlist'(),
if (!(p instanceof Playlist)) {
    throw new Error("Expected a Playlist instance");
}

export {};

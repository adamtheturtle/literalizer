class Playlist {
    constructor(_options: object = {}) {}
}

static _VVal p = Playlist();
if (!(p instanceof Playlist)) {
    throw new Error("Expected a Playlist instance");
}

export {};

class Playlist {
    constructor(_options: object = {}) {}
}

protected Object p = new Playlist();
if (!(p instanceof Playlist)) {
    throw new Error("Expected a Playlist instance");
}

export {};

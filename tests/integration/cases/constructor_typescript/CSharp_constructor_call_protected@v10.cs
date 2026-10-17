class Playlist {
    constructor(_options: object = {}) {}
}

protected object? p = new Playlist();
if (!(p instanceof Playlist)) {
    throw new Error("Expected a Playlist instance");
}

export {};

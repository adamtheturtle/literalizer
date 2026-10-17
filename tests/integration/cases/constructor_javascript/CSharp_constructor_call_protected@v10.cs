class Playlist {
    constructor(_options = {}) {}
}

protected object? p = new Playlist();
if (!(p instanceof Playlist)) {
    throw new Error("Expected a Playlist instance");
}

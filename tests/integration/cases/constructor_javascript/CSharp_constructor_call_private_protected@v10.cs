class Playlist {
    constructor(_options = {}) {}
}

private protected object? p = new Playlist();
if (!(p instanceof Playlist)) {
    throw new Error("Expected a Playlist instance");
}

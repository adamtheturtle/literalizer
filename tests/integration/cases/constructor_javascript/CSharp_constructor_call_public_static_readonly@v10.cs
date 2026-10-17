class Playlist {
    constructor(_options = {}) {}
}

public static readonly object? p = new Playlist();
if (!(p instanceof Playlist)) {
    throw new Error("Expected a Playlist instance");
}

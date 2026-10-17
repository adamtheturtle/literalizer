class Playlist {
    constructor(_options = {}) {}
}

Dim p = New Playlist()
if (!(p instanceof Playlist)) {
    throw new Error("Expected a Playlist instance");
}

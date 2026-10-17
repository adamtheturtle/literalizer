class Playlist {
    constructor(_options = {}) {}
}

val p = Playlist()
if (!(p instanceof Playlist)) {
    throw new Error("Expected a Playlist instance");
}

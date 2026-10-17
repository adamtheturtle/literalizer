class Playlist {
    constructor(_options = {}) {}
}

(def p (Playlist))
if (!(p instanceof Playlist)) {
    throw new Error("Expected a Playlist instance");
}

class Playlist {
    constructor(_options = {}) {}
}

(define p (Playlist))
if (!(p instanceof Playlist)) {
    throw new Error("Expected a Playlist instance");
}

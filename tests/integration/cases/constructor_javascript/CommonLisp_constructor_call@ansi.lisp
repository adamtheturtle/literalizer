class Playlist {
    constructor(_options = {}) {}
}

(defparameter *p* (Playlist))
if (!(p instanceof Playlist)) {
    throw new Error("Expected a Playlist instance");
}

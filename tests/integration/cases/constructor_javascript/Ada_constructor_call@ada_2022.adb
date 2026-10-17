class Playlist {
    constructor(_options = {}) {}
}

p : A_Val := Playlist;
if (!(p instanceof Playlist)) {
    throw new Error("Expected a Playlist instance");
}

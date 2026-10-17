class Playlist {
    constructor(_options = {}) {}
}

data Val
    = PList (Array Val)
p = Playlist
if (!(p instanceof Playlist)) {
    throw new Error("Expected a Playlist instance");
}

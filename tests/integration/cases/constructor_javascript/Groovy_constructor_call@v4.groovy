class Playlist {
    constructor(_options = {}) {}
}

def p = new Playlist()
if (!(p instanceof Playlist)) {
    throw new Error("Expected a Playlist instance");
}

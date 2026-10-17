class Playlist {
    constructor(_options = {}) {}
}

local p = Playlist()
if (!(p instanceof Playlist)) {
    throw new Error("Expected a Playlist instance");
}

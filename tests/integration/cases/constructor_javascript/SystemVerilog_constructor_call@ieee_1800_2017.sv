class Playlist {
    constructor(_options = {}) {}
}

static _VVal p = Playlist();
if (!(p instanceof Playlist)) {
    throw new Error("Expected a Playlist instance");
}

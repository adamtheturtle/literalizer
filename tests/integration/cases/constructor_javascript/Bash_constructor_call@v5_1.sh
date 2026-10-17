class Playlist {
    constructor(_options = {}) {}
}

declare p="$(Playlist)"
if (!(p instanceof Playlist)) {
    throw new Error("Expected a Playlist instance");
}

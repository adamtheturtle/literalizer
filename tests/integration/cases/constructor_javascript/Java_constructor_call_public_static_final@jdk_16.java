class Playlist {
    constructor(_options = {}) {}
}

public static final Object p = new Playlist();
if (!(p instanceof Playlist)) {
    throw new Error("Expected a Playlist instance");
}

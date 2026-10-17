class Playlist {
    constructor(_options = {}) {}
}

datatype val_t =
    SList of val_t list
val p = Playlist()
if (!(p instanceof Playlist)) {
    throw new Error("Expected a Playlist instance");
}

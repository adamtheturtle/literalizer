class Playlist {
    constructor(_options: object = {}) {}
}

type val_t =
  | OList of val_t list
let p = Playlist
if (!(p instanceof Playlist)) {
    throw new Error("Expected a Playlist instance");
}

export {};

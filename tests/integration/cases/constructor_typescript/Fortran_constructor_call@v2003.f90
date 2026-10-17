class Playlist {
    constructor(_options: object = {}) {}
}

type(fval_t) :: p
p = Playlist()
if (!(p instanceof Playlist)) {
    throw new Error("Expected a Playlist instance");
}

export {};

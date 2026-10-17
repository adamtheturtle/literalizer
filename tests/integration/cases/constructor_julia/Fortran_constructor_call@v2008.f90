struct Playlist end

type(fval_t) :: p
p = Playlist()
@assert p isa Playlist

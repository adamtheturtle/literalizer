type Playlist = object
    value: int

type(fval_t) :: p
p = Playlist()
doAssert p.value == 0

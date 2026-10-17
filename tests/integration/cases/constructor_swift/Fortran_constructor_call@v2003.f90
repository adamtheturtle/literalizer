struct Playlist { let value = 42 }

type(fval_t) :: p
p = Playlist()
precondition(p.value == 42)

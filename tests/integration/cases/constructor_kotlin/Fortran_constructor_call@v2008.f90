class Playlist { val value = 42 }

type(fval_t) :: p
p = Playlist()
check(p.value == 42)

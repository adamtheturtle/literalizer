function Playlist { return 42 }

type(fval_t) :: p
p = Playlist()
if ($p -ne 42) { throw "Expected constructor result" }

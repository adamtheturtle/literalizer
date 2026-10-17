proc Playlist {} { return 42 }

type(fval_t) :: p
p = Playlist()
if {$p != 42} { error "Expected constructor result" }

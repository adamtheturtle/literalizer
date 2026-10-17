: Playlist 42 ;

type(fval_t) :: p
p = Playlist()
: check-constructor p 42 <> abort" Expected constructor result" ;
check-constructor

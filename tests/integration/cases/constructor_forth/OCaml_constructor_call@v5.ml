: Playlist 42 ;

type val_t =
  | OList of val_t list
let p = Playlist()
: check-constructor p 42 <> abort" Expected constructor result" ;
check-constructor

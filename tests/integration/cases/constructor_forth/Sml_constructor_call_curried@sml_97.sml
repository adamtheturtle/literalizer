: Playlist 42 ;

datatype val_t =
    SList of val_t list
val p = Playlist
: check-constructor p 42 <> abort" Expected constructor result" ;
check-constructor

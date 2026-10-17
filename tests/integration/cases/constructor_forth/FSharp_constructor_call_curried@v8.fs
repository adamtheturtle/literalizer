: Playlist 42 ;

type Val =
    | FList of Val list
let p = Playlist
: check-constructor p 42 <> abort" Expected constructor result" ;
check-constructor

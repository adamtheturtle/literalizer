: Playlist 42 ;

data Val
    = PList (Array Val)
p = Playlist
: check-constructor p 42 <> abort" Expected constructor result" ;
check-constructor

struct Playlist end

data Val
    = PList (Array Val)
p = Playlist
@assert p isa Playlist

struct Playlist end

data Val = HList [Val]
p = Playlist
@assert p isa Playlist

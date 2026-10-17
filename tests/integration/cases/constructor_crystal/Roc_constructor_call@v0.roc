module ConstructorBinding
class Playlist
end

Val : [
    RList (List Val),
]
p = Playlist
raise "Expected a Playlist instance" unless p.is_a?(Playlist)
end

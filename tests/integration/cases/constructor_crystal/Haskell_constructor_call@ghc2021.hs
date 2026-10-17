module ConstructorBinding
class Playlist
end

data Val = HList [Val]
p = Playlist
raise "Expected a Playlist instance" unless p.is_a?(Playlist)
end

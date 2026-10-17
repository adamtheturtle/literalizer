module ConstructorBinding
class Playlist
end

set p [Playlist]
raise "Expected a Playlist instance" unless p.is_a?(Playlist)
end

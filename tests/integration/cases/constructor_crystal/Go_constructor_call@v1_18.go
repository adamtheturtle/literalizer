module ConstructorBinding
class Playlist
end

p := NewPlaylist()
raise "Expected a Playlist instance" unless p.is_a?(Playlist)
end

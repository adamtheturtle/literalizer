module ConstructorBinding
class Playlist
end

p = Playlist.new()
raise "Expected a Playlist instance" unless p.is_a?(Playlist)
end

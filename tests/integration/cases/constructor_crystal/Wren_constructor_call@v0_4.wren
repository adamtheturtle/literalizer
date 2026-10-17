module ConstructorBinding
class Playlist
end

var p = Playlist.new()
raise "Expected a Playlist instance" unless p.is_a?(Playlist)
end

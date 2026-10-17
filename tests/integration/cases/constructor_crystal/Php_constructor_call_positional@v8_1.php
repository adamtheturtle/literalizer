module ConstructorBinding
class Playlist
end

$p = new Playlist();
raise "Expected a Playlist instance" unless p.is_a?(Playlist)
end

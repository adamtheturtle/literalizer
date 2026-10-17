module ConstructorBinding
class Playlist
end

static const auto p = Playlist();
raise "Expected a Playlist instance" unless p.is_a?(Playlist)
end

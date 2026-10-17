module ConstructorBinding
class Playlist
end

static Object p = new Playlist();
raise "Expected a Playlist instance" unless p.is_a?(Playlist)
end

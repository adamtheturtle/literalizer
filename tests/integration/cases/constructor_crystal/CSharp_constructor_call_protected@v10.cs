module ConstructorBinding
class Playlist
end

protected object? p = new Playlist();
raise "Expected a Playlist instance" unless p.is_a?(Playlist)
end

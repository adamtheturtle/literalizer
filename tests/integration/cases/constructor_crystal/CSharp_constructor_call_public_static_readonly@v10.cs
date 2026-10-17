module ConstructorBinding
class Playlist
end

public static readonly object? p = new Playlist();
raise "Expected a Playlist instance" unless p.is_a?(Playlist)
end

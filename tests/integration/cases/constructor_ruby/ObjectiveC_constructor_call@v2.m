class Playlist
end

id p = Playlist();
raise "Expected a Playlist instance" unless p.is_a?(Playlist)

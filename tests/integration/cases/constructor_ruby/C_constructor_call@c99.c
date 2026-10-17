class Playlist
end

CVal p = Playlist();
raise "Expected a Playlist instance" unless p.is_a?(Playlist)

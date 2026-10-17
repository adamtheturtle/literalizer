class Playlist
end

val p = new Playlist()
raise "Expected a Playlist instance" unless p.is_a?(Playlist)

module ConstructorBinding
class Playlist
end

Dim p = New Playlist()
raise "Expected a Playlist instance" unless p.is_a?(Playlist)
end

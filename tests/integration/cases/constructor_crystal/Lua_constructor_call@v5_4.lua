module ConstructorBinding
class Playlist
end

local p = Playlist()
raise "Expected a Playlist instance" unless p.is_a?(Playlist)
end

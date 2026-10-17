module ConstructorBinding
class Playlist
end

P = 'Playlist'(),
raise "Expected a Playlist instance" unless p.is_a?(Playlist)
end

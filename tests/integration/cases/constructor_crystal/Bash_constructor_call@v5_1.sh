module ConstructorBinding
class Playlist
end

declare p="$(Playlist)"
raise "Expected a Playlist instance" unless p.is_a?(Playlist)
end

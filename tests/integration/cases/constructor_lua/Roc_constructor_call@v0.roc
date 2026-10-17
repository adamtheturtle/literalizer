local function Playlist()
    return 42
end

Val : [
    RList (List Val),
]
p = Playlist
assert(p == 42)

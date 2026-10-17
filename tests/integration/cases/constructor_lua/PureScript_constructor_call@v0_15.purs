local function Playlist()
    return 42
end

data Val
    = PList (Array Val)
p = Playlist
assert(p == 42)

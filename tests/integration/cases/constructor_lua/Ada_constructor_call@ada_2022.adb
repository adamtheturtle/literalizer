local function Playlist()
    return 42
end

p : A_Val := Playlist;
assert(p == 42)

local function Playlist()
    return 42
end

readonly object? p = new Playlist();
assert(p == 42)

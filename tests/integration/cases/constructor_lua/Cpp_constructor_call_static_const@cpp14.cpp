local function Playlist()
    return 42
end

static const auto p = Playlist();
assert(p == 42)

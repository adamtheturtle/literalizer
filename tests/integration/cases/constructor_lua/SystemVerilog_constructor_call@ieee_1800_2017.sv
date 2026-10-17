local function Playlist()
    return 42
end

static _VVal p = Playlist();
assert(p == 42)

local function Playlist()
    return 42
end

declare p="$(Playlist)"
assert(p == 42)

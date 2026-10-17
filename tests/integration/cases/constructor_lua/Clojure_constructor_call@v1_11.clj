local function Playlist()
    return 42
end

(def p (Playlist))
assert(p == 42)

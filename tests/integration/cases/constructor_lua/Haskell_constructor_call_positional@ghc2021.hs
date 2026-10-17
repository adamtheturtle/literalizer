local function Playlist()
    return 42
end

data Val = HList [Val]
p = Playlist()
assert(p == 42)

local function Playlist()
    return 42
end

type Val =
    | FList of Val list
let p = Playlist()
assert(p == 42)

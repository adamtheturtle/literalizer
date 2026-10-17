local function Playlist()
    return 42
end

type(fval_t) :: p
p = Playlist()
assert(p == 42)

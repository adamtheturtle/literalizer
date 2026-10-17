local function Playlist()
    return 42
end

datatype val_t =
    SList of val_t list
val p = Playlist
assert(p == 42)

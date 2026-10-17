local function Playlist()
    return 42
end

type val_t =
  | OList of val_t list
let p = Playlist()
assert(p == 42)

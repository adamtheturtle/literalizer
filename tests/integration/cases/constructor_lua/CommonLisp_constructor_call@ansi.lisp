local function Playlist()
    return 42
end

(defparameter *p* (Playlist))
assert(p == 42)

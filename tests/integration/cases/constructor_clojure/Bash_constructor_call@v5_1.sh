(defn Playlist [] 42)

declare p="$(Playlist)"
(assert (= p 42))

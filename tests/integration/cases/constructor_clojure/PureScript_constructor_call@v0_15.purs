(defn Playlist [] 42)

data Val
    = PList (Array Val)
p = Playlist
(assert (= p 42))

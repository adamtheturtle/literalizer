(defn Playlist [] 42)

type val_t =
  | OList of val_t list
let p = Playlist
(assert (= p 42))

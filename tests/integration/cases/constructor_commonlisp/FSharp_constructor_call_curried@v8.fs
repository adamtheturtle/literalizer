(defun Playlist () 42)

type Val =
    | FList of Val list
let p = Playlist
(assert (= *p* 42))

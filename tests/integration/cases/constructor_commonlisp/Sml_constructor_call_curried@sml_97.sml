(defun Playlist () 42)

datatype val_t =
    SList of val_t list
val p = Playlist
(assert (= *p* 42))

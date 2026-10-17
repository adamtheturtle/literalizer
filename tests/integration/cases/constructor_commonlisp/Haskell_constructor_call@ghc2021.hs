(defun Playlist () 42)

data Val = HList [Val]
p = Playlist
(assert (= *p* 42))

(defun Playlist () 42)

type(fval_t) :: p
p = Playlist()
(assert (= *p* 42))

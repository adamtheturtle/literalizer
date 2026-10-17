(import (scheme base))

(define (Playlist) 42)

type val_t =
  | OList of val_t list
let p = Playlist()
(unless (= p 42) (error "Expected constructor result"))

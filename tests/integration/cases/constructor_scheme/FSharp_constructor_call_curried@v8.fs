(import (scheme base))

(define (Playlist) 42)

type Val =
    | FList of Val list
let p = Playlist
(unless (= p 42) (error "Expected constructor result"))

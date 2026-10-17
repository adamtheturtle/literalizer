(import (scheme base))

(define (Playlist) 42)

let p = Playlist()
(unless (= p 42) (error "Expected constructor result"))

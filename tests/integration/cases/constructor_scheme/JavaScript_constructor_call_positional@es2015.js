(import (scheme base))

(define (Playlist) 42)

const p = new Playlist();
(unless (= p 42) (error "Expected constructor result"))

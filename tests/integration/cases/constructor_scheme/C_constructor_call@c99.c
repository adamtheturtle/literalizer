(import (scheme base))

(define (Playlist) 42)

CVal p = Playlist();
(unless (= p 42) (error "Expected constructor result"))

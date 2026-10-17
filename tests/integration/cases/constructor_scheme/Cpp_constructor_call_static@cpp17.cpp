(import (scheme base))

(define (Playlist) 42)

static auto p = Playlist();
(unless (= p 42) (error "Expected constructor result"))

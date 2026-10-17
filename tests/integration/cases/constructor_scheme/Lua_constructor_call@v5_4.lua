(import (scheme base))

(define (Playlist) 42)

local p = Playlist()
(unless (= p 42) (error "Expected constructor result"))

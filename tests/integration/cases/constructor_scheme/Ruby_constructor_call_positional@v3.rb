(import (scheme base))

(define (Playlist) 42)

p = Playlist.new()
(unless (= p 42) (error "Expected constructor result"))

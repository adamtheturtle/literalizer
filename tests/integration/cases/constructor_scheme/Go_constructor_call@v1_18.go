(import (scheme base))

(define (Playlist) 42)

p := NewPlaylist()
(unless (= p 42) (error "Expected constructor result"))

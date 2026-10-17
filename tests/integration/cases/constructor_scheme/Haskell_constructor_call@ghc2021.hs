(import (scheme base))

(define (Playlist) 42)

data Val = HList [Val]
p = Playlist
(unless (= p 42) (error "Expected constructor result"))

#lang racket

(define (Playlist) 42)

type(fval_t) :: p
p = Playlist()
(unless (= p 42) (error "Expected constructor result"))

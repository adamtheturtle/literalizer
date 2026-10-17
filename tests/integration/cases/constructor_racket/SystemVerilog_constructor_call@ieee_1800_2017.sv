#lang racket

(define (Playlist) 42)

static _VVal p = Playlist();
(unless (= p 42) (error "Expected constructor result"))

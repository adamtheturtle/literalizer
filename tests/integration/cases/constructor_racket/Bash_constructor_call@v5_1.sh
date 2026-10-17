#lang racket

(define (Playlist) 42)

declare p="$(Playlist)"
(unless (= p 42) (error "Expected constructor result"))

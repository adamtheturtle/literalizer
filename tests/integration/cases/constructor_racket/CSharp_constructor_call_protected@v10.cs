#lang racket

(define (Playlist) 42)

protected object? p = new Playlist();
(unless (= p 42) (error "Expected constructor result"))

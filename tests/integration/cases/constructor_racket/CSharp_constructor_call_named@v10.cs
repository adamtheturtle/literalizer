#lang racket

(define (Playlist) 42)

var p = new Playlist();
(unless (= p 42) (error "Expected constructor result"))

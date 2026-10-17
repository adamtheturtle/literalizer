#lang racket

(define (Playlist) 42)

static object? p = new Playlist();
(unless (= p 42) (error "Expected constructor result"))

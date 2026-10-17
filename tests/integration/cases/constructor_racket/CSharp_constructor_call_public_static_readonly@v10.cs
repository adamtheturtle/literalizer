#lang racket

(define (Playlist) 42)

public static readonly object? p = new Playlist();
(unless (= p 42) (error "Expected constructor result"))

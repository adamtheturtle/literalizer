#lang racket

(define (Playlist) 42)

static const auto p = Playlist();
(unless (= p 42) (error "Expected constructor result"))

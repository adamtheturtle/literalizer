#lang racket

(define (Playlist) 42)

my $p = Playlist();
(unless (= p 42) (error "Expected constructor result"))

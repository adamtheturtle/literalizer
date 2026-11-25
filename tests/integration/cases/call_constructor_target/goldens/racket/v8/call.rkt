#lang racket
(define Playlist (make-keyword-procedure (lambda _ (void))))
(define Playlist.new (make-keyword-procedure (lambda _ (void))))
(Playlist.new #:x 1)

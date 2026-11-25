#lang racket
(define Playlist (make-keyword-procedure (lambda _ (void))))
(define Playlist.newValue (make-keyword-procedure (lambda _ (void))))
(Playlist.newValue #:x 1)

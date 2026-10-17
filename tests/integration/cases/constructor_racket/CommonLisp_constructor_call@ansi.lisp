#lang racket

(define (Playlist) 42)

(defparameter *p* (Playlist))
(unless (= p 42) (error "Expected constructor result"))

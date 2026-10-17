#lang racket

(define (Playlist) 42)

datatype val_t =
    SList of val_t list
val p = Playlist()
(unless (= p 42) (error "Expected constructor result"))

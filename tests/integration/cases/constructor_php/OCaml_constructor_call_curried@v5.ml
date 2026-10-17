<?php
class Playlist {}

type val_t =
  | OList of val_t list
let p = Playlist
if (!($p instanceof Playlist)) {
    throw new Exception("Expected a Playlist instance");
}

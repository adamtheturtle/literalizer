<?php
class Playlist {}

datatype val_t =
    SList of val_t list
val p = Playlist()
if (!($p instanceof Playlist)) {
    throw new Exception("Expected a Playlist instance");
}

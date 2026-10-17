<?php
class Playlist {}

type Val =
    | FList of Val list
let p = Playlist
if (!($p instanceof Playlist)) {
    throw new Exception("Expected a Playlist instance");
}

<?php
class Playlist {}

let p = Playlist::new();
if (!($p instanceof Playlist)) {
    throw new Exception("Expected a Playlist instance");
}

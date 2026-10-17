<?php
class Playlist {}

let p = Playlist()
if (!($p instanceof Playlist)) {
    throw new Exception("Expected a Playlist instance");
}

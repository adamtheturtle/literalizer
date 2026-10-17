<?php
class Playlist {}

p := NewPlaylist()
if (!($p instanceof Playlist)) {
    throw new Exception("Expected a Playlist instance");
}

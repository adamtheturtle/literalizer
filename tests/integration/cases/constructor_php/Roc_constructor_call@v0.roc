<?php
class Playlist {}

Val : [
    RList (List Val),
]
p = Playlist
if (!($p instanceof Playlist)) {
    throw new Exception("Expected a Playlist instance");
}

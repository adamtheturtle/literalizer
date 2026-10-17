<?php
class Playlist {}

(def p (Playlist))
if (!($p instanceof Playlist)) {
    throw new Exception("Expected a Playlist instance");
}

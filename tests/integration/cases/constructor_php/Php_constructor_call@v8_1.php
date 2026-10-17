<?php
class Playlist {}

$p = new Playlist();
if (!($p instanceof Playlist)) {
    throw new Exception("Expected a Playlist instance");
}

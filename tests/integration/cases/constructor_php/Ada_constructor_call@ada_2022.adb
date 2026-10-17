<?php
class Playlist {}

p : A_Val := Playlist;
if (!($p instanceof Playlist)) {
    throw new Exception("Expected a Playlist instance");
}

<?php
class Playlist {}

data Val = HList [Val]
p = Playlist
if (!($p instanceof Playlist)) {
    throw new Exception("Expected a Playlist instance");
}

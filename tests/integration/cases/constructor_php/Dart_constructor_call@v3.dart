<?php
class Playlist {}

final p = Playlist();
if (!($p instanceof Playlist)) {
    throw new Exception("Expected a Playlist instance");
}

<?php
class Playlist {}

declare p="$(Playlist)"
if (!($p instanceof Playlist)) {
    throw new Exception("Expected a Playlist instance");
}

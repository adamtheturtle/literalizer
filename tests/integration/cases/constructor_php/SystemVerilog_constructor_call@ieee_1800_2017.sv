<?php
class Playlist {}

static _VVal p = Playlist();
if (!($p instanceof Playlist)) {
    throw new Exception("Expected a Playlist instance");
}

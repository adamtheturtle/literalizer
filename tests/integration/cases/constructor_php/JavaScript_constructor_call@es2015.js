<?php
class Playlist {}

const p = new Playlist({  });
if (!($p instanceof Playlist)) {
    throw new Exception("Expected a Playlist instance");
}

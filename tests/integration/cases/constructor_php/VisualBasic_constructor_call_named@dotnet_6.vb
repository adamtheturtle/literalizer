<?php
class Playlist {}

Dim p = New Playlist()
if (!($p instanceof Playlist)) {
    throw new Exception("Expected a Playlist instance");
}

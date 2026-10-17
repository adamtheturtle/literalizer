<?php
class Playlist {}

private object? p = new Playlist();
if (!($p instanceof Playlist)) {
    throw new Exception("Expected a Playlist instance");
}

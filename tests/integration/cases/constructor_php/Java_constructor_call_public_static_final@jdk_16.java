<?php
class Playlist {}

public static final Object p = new Playlist();
if (!($p instanceof Playlist)) {
    throw new Exception("Expected a Playlist instance");
}

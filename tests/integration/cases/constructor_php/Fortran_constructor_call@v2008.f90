<?php
class Playlist {}

type(fval_t) :: p
p = Playlist()
if (!($p instanceof Playlist)) {
    throw new Exception("Expected a Playlist instance");
}

<?php
function f($a) {}
function repr($_arg) {}
$ref_data = 1;
repr(f(a: $ref_data));

<?php
class OuterType { function inner($outer, $n) {} }
$outer = new OuterType();
$outer->inner(outer: 1, n: 2);

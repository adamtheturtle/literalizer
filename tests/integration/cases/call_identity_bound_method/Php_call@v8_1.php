<?php
class ThingType { function go($value) {} }
$thing = new ThingType();
$item = [
    1,
    2,
];
$thing->go(value: $item);

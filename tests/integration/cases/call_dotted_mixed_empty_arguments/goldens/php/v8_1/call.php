<?php
class ThingType { function go($before, $populated, $after) {} }
$thing = new ThingType();
$thing->go(before: [], populated: [1], after: []);
$thing->go(before: ["text"], populated: [2], after: []);
$thing->go(before: [], populated: ["text"], after: []);
$thing->go(before: ["text"], populated: [2], after: [3]);

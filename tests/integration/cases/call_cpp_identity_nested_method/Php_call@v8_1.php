<?php
class ThingType { function go() {} }
class OuterType { public $thing; function __construct() { $this->thing = new ThingType(); } }
$outer = new OuterType();
$outer->thing->go();

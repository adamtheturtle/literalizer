<?php
class FoobarType { function bar($x) {} }
class Foo_barType { public $fooBar; function __construct() { $this->fooBar = new FoobarType(); } }
class AType { public $foo_bar; function __construct() { $this->foo_bar = new Foo_barType(); } }
$a = new AType();
$a->foo_bar->fooBar->bar(x: [1]);

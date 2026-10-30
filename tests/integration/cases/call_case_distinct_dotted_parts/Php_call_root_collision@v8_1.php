<?php
class FooType { function bar($x) {} }
class FooType { public $Foo; function __construct() { $this->Foo = new FooType(); } }
$foo = new FooType();
$foo->Foo->bar(x: [1]);

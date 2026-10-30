<?php
class FooType { function bar($x) {} }
class FooType { public $Foo; function __construct() { $this->Foo = new FooType(); } }
class AType { public $foo; function __construct() { $this->foo = new FooType(); } }
$a = new AType();
$my_data = $a->foo->Foo->bar(x: [1]);

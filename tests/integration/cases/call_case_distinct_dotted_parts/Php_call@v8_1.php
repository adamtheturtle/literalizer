<?php
class FooType2 { function bar($x) {} }
class FooType1 { public $Foo; function __construct() { $this->Foo = new FooType2(); } }
class AType { public $foo; function __construct() { $this->foo = new FooType1(); } }
$a = new AType();
$a->foo->Foo->bar(x: [1]);

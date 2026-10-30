<?php
class FooType1 { function bar($x) {} }
class FooType0 { public $Foo; function __construct() { $this->Foo = new FooType1(); } }
$foo = new FooType0();
$foo->Foo->bar(x: [1]);

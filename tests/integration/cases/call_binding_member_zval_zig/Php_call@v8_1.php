<?php
class ObjType { function ZVal($_arg) {} }
$obj = new ObjType();
$my_data = $obj->ZVal(_arg: 42) // note;

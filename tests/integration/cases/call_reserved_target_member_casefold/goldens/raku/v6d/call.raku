class ObjType { method BEGIN(*@a, *%kw) {} }
my $obj = ObjType.bless;
$obj.BEGIN(42);

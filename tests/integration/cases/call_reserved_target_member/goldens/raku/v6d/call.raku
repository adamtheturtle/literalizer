class ObjType { method class(*@a, *%kw) {} }
my $obj = ObjType.bless;
$obj.class(42);

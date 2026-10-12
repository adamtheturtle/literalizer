class ObjType { method ZVal(*@a, *%kw) {} }
my $obj = ObjType.bless;
my $my_data = $obj.ZVal(42) // note;

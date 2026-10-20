class ThingType { method go(*@a, *%kw) {} }
class OuterType { method thing { ThingType.bless } }
my $outer = OuterType.bless;
$outer.thing.go();

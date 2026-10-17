class ThingType { method first_value(*@a, *%kw) {} }
my $thing = ThingType.bless;
$thing.first_value(1);

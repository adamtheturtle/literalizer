class ThingType { method go(*@a, *%kw) {} }
my $thing = ThingType.bless;
my $my_data = $thing.go([]);

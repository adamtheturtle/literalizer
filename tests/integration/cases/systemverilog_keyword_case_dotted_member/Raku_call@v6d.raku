class ThingType { method Before(*@a, *%kw) {} }
my $thing = ThingType.bless;
$thing.Before(1);

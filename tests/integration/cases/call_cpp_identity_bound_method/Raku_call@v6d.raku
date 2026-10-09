class ThingType { method go(*@a, *%kw) {} }
my $thing = ThingType.bless;
my $item = [
    1,
    2,
];
$thing.go($item);

sub f(*@a, *%kw) {}
my $ref_data = [
    1,
    2,
];
f([
    $ref_data,
]);
f([
    $ref_data,
]);

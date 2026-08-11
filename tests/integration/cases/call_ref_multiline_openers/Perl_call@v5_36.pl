sub consume {}
my $foo = 42;
consume([
    {
        "other" => 1,
    },
    $foo,
], {
    "left" => $foo,
    "other" => 1,
});

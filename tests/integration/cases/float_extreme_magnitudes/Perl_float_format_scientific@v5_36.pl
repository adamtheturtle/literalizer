use Math::BigFloat;
my $my_data = [
    (0.0 + 5.0e-324),
    (0.0 + 2.2250738585072014e-308),
    (0.0 + 1.0e-307),
    Math::BigFloat->new("1.0e21"),
    Math::BigFloat->new("-1.5e300"),
    Math::BigFloat->new("1.7976931348623157e308"),
    Math::BigFloat->new("-1.7976931348623157e308"),
];

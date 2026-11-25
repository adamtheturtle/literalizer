class ThrottlerType { method check(*@a, *%kw) {} }
my $throttler = ThrottlerType.bless;
$throttler.check();
$throttler.check();

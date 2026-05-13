class ThrottlerType { method check(*@a, *%kw) {} }
my $throttler = ThrottlerType.new;
$throttler.check();
$throttler.check();

class ThrottlerType { method check(*@a, *%kw) {} }
my $throttler = ThrottlerType.new;
sub emit {}
emit($throttler.check('user_1', 1000.0));
emit($throttler.check('user_2', 2000.5));

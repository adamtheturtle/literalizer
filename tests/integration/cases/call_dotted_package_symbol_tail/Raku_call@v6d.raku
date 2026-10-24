class HelperType { method list(*@a, *%kw) {} }
my $helper = HelperType.bless;
$helper.list(1);

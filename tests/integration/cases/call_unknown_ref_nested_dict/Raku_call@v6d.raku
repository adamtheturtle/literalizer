sub process(*@a, *%kw) {}
my $my_list = [];
process([[{'inner' => $my_list}]]);

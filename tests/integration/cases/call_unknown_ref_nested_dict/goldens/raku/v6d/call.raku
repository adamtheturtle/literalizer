sub process(*@a, *%kw) {}
my $my_list = {
    'unused' => 'value',
};
process([[{'inner' => $my_list},],]);

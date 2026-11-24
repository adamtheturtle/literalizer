sub process {}
my $my_list = {
    "unused" => "value",
};
process([[{"inner" => $my_list}]]);

: process ;
: my_ints
    1
    2
    3
;
: my_strings
    s\" a"
    s\" b"
;
: my_empty ;
my_ints 42 process
my_strings 7 process
my_empty 99 process

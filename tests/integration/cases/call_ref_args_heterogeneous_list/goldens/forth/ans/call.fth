: process ;
: my_ints
+arr
    1 +int
    2 +int
    3 +int
 -arr
;
: my_strings
+arr
    s\" a" +str
    s\" b" +str
 -arr
;
: my_empty +arr -arr ;
my_ints 42 process
my_strings 7 process
my_empty 99 process

: process ;
: my_var
+arr
    1 +int
    2 +int
    3 +int
 -arr
;
: my_other
+arr
    4 +int
    5 +int
    6 +int
 -arr
;
my_var 42 process
my_other 7 process

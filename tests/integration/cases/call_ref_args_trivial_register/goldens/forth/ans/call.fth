: process ;
: my_int 1 +int ;
: my_bool true +bool ;
: my_float 3.14e0 +float ;
: my_list
+arr
    1 +int
    2 +int
    3 +int
 -arr
;
my_int 42 process
my_bool 7 process
my_float 9 process
my_list 1 process

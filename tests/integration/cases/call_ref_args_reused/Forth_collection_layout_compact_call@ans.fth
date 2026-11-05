: process ;
: single_var
+arr
    4 +int
    5 +int
    6 +int
 -arr
;
: repeated_var 1 +int ;
repeated_var 1 process
single_var 0 process
repeated_var 8 process

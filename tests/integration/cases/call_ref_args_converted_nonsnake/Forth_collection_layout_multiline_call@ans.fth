: process ;
: MY_VAR
+arr
    1 +int
    2 +int
    3 +int
 -arr
;
: MY_OTHER
+arr
    4 +int
    5 +int
    6 +int
 -arr
;
MY_VAR 42 process
MY_OTHER 7 process

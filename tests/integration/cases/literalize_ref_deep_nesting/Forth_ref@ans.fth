: DEEP
+arr
    +arr
        1 +int
        2 +int
     -arr
    +arr
        3 +int
        4 +int
     -arr
 -arr
;
: my_data
+obj
    s\" a" +key +obj
        s\" b" +key +obj
            s\" c" +key DEEP
         -obj
     -obj
 -obj
;

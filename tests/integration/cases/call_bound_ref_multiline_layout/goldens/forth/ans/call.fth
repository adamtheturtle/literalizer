: f ;
: ref_data
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
+arr
    +arr
        ref_data
     -arr
 -arr f

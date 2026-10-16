: ref_data
+arr
    1 +int
    2 +int
 -arr
;
: my_data
+arr
    0 +int
 -arr
;
(void)my_data;
: my_data ref_data ;
(void)my_data;

: consume_widget ;
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
my_data consume_widget
: my_data ref_data ;
my_data consume_widget

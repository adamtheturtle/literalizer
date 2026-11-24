: consume_widget ;
: missing
+arr
    1 +int
    2 +int
 -arr
;
: my_data missing ;
my_data consume_widget

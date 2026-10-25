: consume_widget ;
: a 0 +int ;
: my_data
+arr
    a
    1 +int
 -arr
;
my_data consume_widget

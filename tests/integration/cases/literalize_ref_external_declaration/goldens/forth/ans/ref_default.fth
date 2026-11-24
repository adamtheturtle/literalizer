: consume_widget ;
: shared
+arr
    1 +int
    2 +int
 -arr
;
: my_data shared ;
my_data consume_widget

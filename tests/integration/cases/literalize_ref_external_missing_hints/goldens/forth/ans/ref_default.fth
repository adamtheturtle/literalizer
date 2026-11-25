: consume_widget ;
: item
+arr
    1 +int
    2 +int
 -arr
;
: my_data
+arr
    1 +int
    2 +int
 -arr
;
my_data consume_widget
: my_data item ;
my_data consume_widget

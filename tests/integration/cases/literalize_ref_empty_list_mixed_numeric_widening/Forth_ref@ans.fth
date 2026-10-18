: EMPTY_VALUES +arr  -arr ;
: INTEGER_VALUES
+arr
    1 +int
 -arr
;
: FLOAT_VALUES
+arr
    1.5e0 +float
 -arr
;
: my_data
+arr
    EMPTY_VALUES
    INTEGER_VALUES
    FLOAT_VALUES
 -arr
;

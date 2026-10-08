: ACTUAL 42 +int ;
: my_data
+arr
    +obj s\" $ref" +key 1 +int -obj
    +obj s\" $ref" +key +null -obj
    ACTUAL
 -arr
;

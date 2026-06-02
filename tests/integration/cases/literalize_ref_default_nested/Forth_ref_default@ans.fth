: item_var
+obj
    s\" _" +key s\" _" +str
 -obj
;
: my_data
+obj
    s\" items" +key +arr item_var +obj s\" fallback" +key s\" value" +str -obj -arr
 -obj
;

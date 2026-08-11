: FOO
+obj
    s\" _" +key s\" _" +str
 -obj
;
: my_data
+obj
    s\" items" +key +arr +obj s\" other" +key 1 +int -obj FOO -arr
    s\" mapping" +key +obj s\" value" +key FOO -obj
 -obj
;

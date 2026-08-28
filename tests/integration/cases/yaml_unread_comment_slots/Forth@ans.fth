\ Between the key and its value.
\ On the block scalar header.
\ On the alias.
: my_data
+obj
    s\" flow" +key +arr 1 +int 2 +int -arr
    s\" gap" +key 3 +int
    s\" block" +key s\" Text.\n" +str
    s\" nested" +key +arr 1 +int 1 +int -arr
    s\" anchored" +key 4 +int
    s\" alias" +key 4 +int
 -obj
;

: consume ;
: foo 42 +int ;
+arr
    +obj
        s\" other" +key 1 +int
     -obj
    foo
 -arr +obj
    s\" left" +key foo
    s\" other" +key 1 +int
 -obj consume

: DEEP
+arr
    +arr
        s\" one" +str
        s\" two" +str
     -arr
    +arr
        s\" three" +str
        s\" four" +str
     -arr
 -arr
;
: my_data
+obj
    s\" a" +key +obj
        s\" b" +key +obj
            s\" c" +key DEEP
         -obj
     -obj
 -obj
;

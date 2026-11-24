            : SHARED
+arr
                1 +int
                2 +int
             -arr
;
            : OTHER 3 +int ;
            : PAYLOAD s\" \n    shared : Val\nshared = RInt 99" +str ;
            : my_data
+obj
                s\" a" +key SHARED
                s\" b" +key OTHER
                s\" payload" +key PAYLOAD
             -obj
;

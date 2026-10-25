        : SHARED
+arr
            1 +int
            2 +int
         -arr
;
        \ A leading comment with { braces, "quotes", and // markers
        : my_data
+arr
            s\" first\n{ \"quoted\" // text }" +str
            SHARED
         -arr
;

\ strings stay data
\ URL annotation
\ outside the string
: my_data
+arr
    s\" https://example.org/a/*b*/" +str
    s\" escaped quote: \" // still data" +str
    s\" backslash: \\" +str
    s\" /* not a comment */" +str
 -arr
;
\ strings stay data
\ URL annotation
\ outside the string
: my_data
+arr
    s\" https://example.org/a/*b*/" +str
    s\" escaped quote: \" // still data" +str
    s\" backslash: \\" +str
    s\" /* not a comment */" +str
 -arr
;

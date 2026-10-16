\ A JSONC input case with both comment forms.
\ detail
\ continued
\ trailing line comment
: my_data
+obj
    s\" url" +key s\" https://example.org/a/*b*/" +str
    s\" count" +key 2 +int
 -obj
;

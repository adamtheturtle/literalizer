: process ;
: big_list
+arr
    s\" x" +str
 -arr
;
+obj s\" k" +key big_list -obj 2 process

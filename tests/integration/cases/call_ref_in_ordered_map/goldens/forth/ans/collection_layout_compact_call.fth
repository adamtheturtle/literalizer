: process ;
: big_list
+arr
    s\" x" +str
 -arr
;
+obj s\" m" +key big_list -obj process

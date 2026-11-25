: process ;
: my_list
+obj
    s\" unused" +key s\" value" +str
 -obj
;
+arr +arr +obj s\" inner" +key my_list -obj -arr -arr process

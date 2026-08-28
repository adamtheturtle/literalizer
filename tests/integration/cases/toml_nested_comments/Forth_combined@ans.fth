\ About the first dotted key.
\ About the second dotted key.
\ About the plain key.
\ Inside the table.
\ Before the first entry.
\ Before the second entry.
: my_data
+obj
    s\" dotted" +key +obj s\" first" +key 1 +int s\" second" +key 2 +int -obj
    s\" plain" +key 3 +int
    s\" table" +key +obj s\" inner" +key 4 +int -obj
    s\" entries" +key +arr +obj s\" name" +key s\" one" +str -obj +obj s\" name" +key s\" two" +str -obj -arr
 -obj
;
\ About the first dotted key.
\ About the second dotted key.
\ About the plain key.
\ Inside the table.
\ Before the first entry.
\ Before the second entry.
: my_data
+obj
    s\" dotted" +key +obj s\" first" +key 1 +int s\" second" +key 2 +int -obj
    s\" plain" +key 3 +int
    s\" table" +key +obj s\" inner" +key 4 +int -obj
    s\" entries" +key +arr +obj s\" name" +key s\" one" +str -obj +obj s\" name" +key s\" two" +str -obj -arr
 -obj
;

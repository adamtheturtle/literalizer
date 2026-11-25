: app ;
: app.process ;
: app.process.fetch ;
+obj s\" data" +key s\" hello" +str -obj app.process.fetch
+obj s\" data" +key 42 +int -obj app.process.fetch
+obj s\" data" +key true +bool -obj app.process.fetch

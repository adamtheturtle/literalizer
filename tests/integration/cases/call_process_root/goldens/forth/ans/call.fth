: process ;
: process.api ;
: process.api.fetch ;
+obj s\" data" +key s\" hello" +str -obj process.api.fetch
+obj s\" data" +key 42 +int -obj process.api.fetch
+obj s\" data" +key true +bool -obj process.api.fetch

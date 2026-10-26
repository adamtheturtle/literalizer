: api ;
: api.worker ;
: api.worker.process ;
+arr 1 +int +obj -obj -arr 42 api.worker.process
+arr 2 +int +obj s\" x" +key s\" s" +str -obj -arr 43 api.worker.process

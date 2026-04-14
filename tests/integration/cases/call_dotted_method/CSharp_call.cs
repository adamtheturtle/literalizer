using System;
dynamic app = new System.Dynamic.ExpandoObject();
app.client.fetch("hello");
app.client.fetch(42);
app.client.fetch(true);

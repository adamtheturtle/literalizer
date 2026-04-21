using System;
dynamic client = new System.Dynamic.ExpandoObject();
client.api.request("hello");
client.api.request(42);
client.api.request(true);

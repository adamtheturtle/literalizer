using System;
dynamic obj = new System.Dynamic.ExpandoObject();
obj.api.client.post("hello");
obj.api.client.post(42);
obj.api.client.post(true);

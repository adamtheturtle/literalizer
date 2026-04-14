using System;
dynamic ns = new System.Dynamic.ExpandoObject();
ns.client.send("hello");
ns.client.send(42);
ns.client.send(true);

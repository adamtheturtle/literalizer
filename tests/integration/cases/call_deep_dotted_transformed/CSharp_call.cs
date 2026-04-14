using System;
dynamic app = new System.Dynamic.ExpandoObject();
dynamic emit(dynamic a) => null;
emit(app.client.fetch("hello"));
emit(app.client.fetch(42));
emit(app.client.fetch(true));

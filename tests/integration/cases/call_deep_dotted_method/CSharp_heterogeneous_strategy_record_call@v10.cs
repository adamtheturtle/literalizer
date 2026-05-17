using System;
using System.Collections.Generic;
class Check {
class ClientType_ { public object post(object data = null) => null; }
class ApiType_ { public ClientType_ client = new ClientType_(); }
class ObjType_ { public ApiType_ api = new ApiType_(); }
static ObjType_ obj = new ObjType_();
    public static void Main() {
obj.api.client.post("hello");
obj.api.client.post(42);
obj.api.client.post(true);
    }
}

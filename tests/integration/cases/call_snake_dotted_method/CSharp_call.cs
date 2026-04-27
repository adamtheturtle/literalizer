using System;
class Check {
class Http_ClientType_ { public object fetch(object payload = null) => null; }
class My_AppType_ { public Http_ClientType_ http_client = new Http_ClientType_(); }
static My_AppType_ my_app = new My_AppType_();
    public static void Main() {
my_app.http_client.fetch("hello");
my_app.http_client.fetch(42);
my_app.http_client.fetch(true);
    }
}

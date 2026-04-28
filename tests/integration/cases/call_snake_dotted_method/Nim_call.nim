type Http_ClientType_ = object
type My_AppType_ = object
    http_client: Http_ClientType_
proc fetch(self: Http_ClientType_; _args: varargs[untyped]) = discard
var my_app: My_AppType_
my_app.http_client.fetch("hello")
my_app.http_client.fetch(42)
my_app.http_client.fetch(true)

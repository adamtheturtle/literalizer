class My_appHttp_client_ {
    fetch(payload) {}
}
class My_app_ {
    http_client { _http_client }
    construct new() {
        _http_client = My_appHttp_client_.new()
    }
}
var my_app = My_app_.new()
my_app.http_client.fetch("hello")
my_app.http_client.fetch(42)
my_app.http_client.fetch(true)

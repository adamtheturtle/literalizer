class ObjApiClient_ {
    post(data) {}
}
class ObjApi_ {
    client { _client }
    construct new() {
        _client = ObjApiClient_.new()
    }
}
class Obj_ {
    api { _api }
    construct new() {
        _api = ObjApi_.new()
    }
}
var obj = Obj_.new()
obj.api.client.post("hello")
obj.api.client.post(42)
obj.api.client.post(true)

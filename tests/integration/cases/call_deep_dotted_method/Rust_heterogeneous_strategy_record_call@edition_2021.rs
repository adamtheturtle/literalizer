fn main() {
    struct ClientType;
    impl ClientType { fn post<A>(&self, _data: A) {} }
    struct ApiType { client: ClientType }
    struct ObjType { api: ApiType }
    let obj = ObjType { api: ApiType { client: ClientType } };
    obj.api.client.post("hello");
    obj.api.client.post(42);
    obj.api.client.post(true);
}

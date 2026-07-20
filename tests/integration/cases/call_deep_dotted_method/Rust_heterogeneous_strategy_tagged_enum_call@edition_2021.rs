fn main() {
    struct ClientType_;
    impl ClientType_ { fn post<A>(&self, _data: A) {} }
    struct ApiType_ { client: ClientType_ }
    struct ObjType_ { api: ApiType_ }
    let obj = ObjType_ { api: ApiType_ { client: ClientType_ } };
    obj.api.client.post("hello");
    obj.api.client.post(42);
    obj.api.client.post(true);
}

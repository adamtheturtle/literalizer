fn main() {
    struct ApiType_;
    impl ApiType_ { fn request<A>(&self, _data: A) {} }
    struct ClientType_ { api: ApiType_ }
    let client = ClientType_ { api: ApiType_ };
    client.api.request("hello");
    client.api.request(42);
    client.api.request(true);
}

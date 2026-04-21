package main
type apiType_ struct{}
func (apiType_) request(args ...any) any { return nil }
type clientType_ struct{ api apiType_ }
var client clientType_

func main() {
client.api.request("hello");
client.api.request(42);
client.api.request(true);
}

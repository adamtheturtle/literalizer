package main
type clientType_ struct{}
func (clientType_) send(args ...any) any { return nil }
type nsType_ struct{ client clientType_ }
var ns nsType_

func main() {
ns.client.send("hello");
ns.client.send(42);
ns.client.send(true);
}

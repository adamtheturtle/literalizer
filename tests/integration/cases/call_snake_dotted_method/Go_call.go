package main
type http_clientType_ struct{}
func (http_clientType_) fetch(args ...any) any { return nil }
type my_appType_ struct{ http_client http_clientType_ }
var my_app my_appType_

func main() {
my_app.http_client.fetch("hello")
my_app.http_client.fetch(42)
my_app.http_client.fetch(true)
}

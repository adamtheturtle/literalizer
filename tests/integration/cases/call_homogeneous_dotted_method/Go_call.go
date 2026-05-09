package main
type clientType_ struct{}
func (clientType_) fetch(args ...any) any { return nil }
type appType_ struct{ client clientType_ }
var app appType_

func main() {
app.client.fetch("hello")
app.client.fetch("world")
}

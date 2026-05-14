package main
type clientType_ struct{}
func (clientType_) fetch(args ...any) any { return nil }
type appType_ struct{ client clientType_ }
var app appType_
func emit(args ...any) any { return nil }

func main() {
emit(app.client.fetch("hello"))
emit(app.client.fetch(42))
emit(app.client.fetch(true))
}

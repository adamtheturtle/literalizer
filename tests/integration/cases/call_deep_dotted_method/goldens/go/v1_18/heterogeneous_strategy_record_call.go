package main
type clientType_ struct{}
func (clientType_) post(args ...any) any { return nil }
type apiType_ struct{ client clientType_ }
type objType_ struct{ api apiType_ }
var obj objType_

func main() {
obj.api.client.post("hello")
obj.api.client.post(42)
obj.api.client.post(true)
}

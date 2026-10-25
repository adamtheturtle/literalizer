package main
func process(args ...any) any { return nil }
type helpersType_ struct{}
func (helpersType_) emit(args ...any) any { return nil }
var helpers helpersType_

func main() {
helpers.emit(process(1), 42)
}

package main
type thingType_ struct{}
func (thingType_) go(args ...any) any { return nil }
var thing thingType_

func main() {
thing.go()
}

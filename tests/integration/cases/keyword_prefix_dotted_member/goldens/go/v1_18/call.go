package main
type thingType_ struct{}
func (thingType_) first_value(args ...any) any { return nil }
var thing thingType_

func main() {
thing.first_value(1)
}

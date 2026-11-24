package main
type thingType_ struct{}
func (thingType_) Before(args ...any) any { return nil }
var thing thingType_

func main() {
thing.Before(1)
}

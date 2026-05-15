package main
func process(args ...any) any { return nil }
type tracerType_ struct{}
func (tracerType_) emit(args ...any) any { return nil }
var tracer tracerType_

func main() {
tracer.emit(process("hello"))
tracer.emit(process(42))
tracer.emit(process(true))
}

package main
func process(args ...any) any { return nil }
type logType_ struct{}
func (logType_) emit(args ...any) any { return nil }
var log logType_

func main() {
log.emit(process("hello"));
log.emit(process(42));
log.emit(process(true));
}

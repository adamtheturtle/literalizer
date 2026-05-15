function process {}
class TracerType_ { [object] emit([object] $_arg) { return $null } }
$tracer = [TracerType_]::new()
tracer.emit(process("hello"))
tracer.emit(process(42))
tracer.emit(process($true))

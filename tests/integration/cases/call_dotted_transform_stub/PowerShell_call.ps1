function process {}
class LogType_ { [object] emit([object] $_arg) { return $null } }
$log = [LogType_]::new()
log.emit(process("hello"))
log.emit(process(42))
log.emit(process($true))

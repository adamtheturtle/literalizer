using System;
class Check {
static object process(object value = null) => null;
class LogType_ { public object emit(object _arg = null) => null; }
static LogType_ log = new LogType_();
    public static void Main() {
log.emit(process("hello"));
log.emit(process(42));
log.emit(process(true));
    }
}

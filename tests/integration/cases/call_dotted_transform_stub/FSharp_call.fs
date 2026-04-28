module Main

type Val =
    | FBool of bool
    | FInt of int64
    | FStr of string
    | FList of Val list
let process (_value: obj) : obj = null
type LogType_() =
    member _.emit(__arg: obj) : obj = null
let log = LogType_()
log.emit(process("hello"))
log.emit(process(42))
log.emit(process(FBool true))

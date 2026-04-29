module Main

type Val =
    | FBool of bool
    | FInt of int64
    | FStr of string
    | FList of Val list
let process (_value: obj) : obj = null
type TracerType_() =
    member _.emit(__arg: obj) : obj = null
let tracer = TracerType_()
tracer.emit(process("hello"))
tracer.emit(process(42))
tracer.emit(process(FBool true))

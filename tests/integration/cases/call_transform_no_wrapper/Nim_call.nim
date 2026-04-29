template process(args: varargs[untyped]): untyped {.discardable.} = 0
process("hello")
process(42)
process(true)

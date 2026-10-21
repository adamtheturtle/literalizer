template process(args: varargs[untyped]) = discard
process(1, "hello")
process("two", false)
process(3.5, nil)

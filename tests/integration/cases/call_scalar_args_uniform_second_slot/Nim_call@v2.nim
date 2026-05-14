template process(args: varargs[untyped]) = discard
process("hello", "a")
process(42, "b")
process(true, "c")

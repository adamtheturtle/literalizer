template f(args: varargs[untyped]) = discard
f(2, "hello")  # trailing note
# next element
f(3, "world")

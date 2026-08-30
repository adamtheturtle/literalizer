template f(args: varargs[untyped]) = discard
f([["DEL", "b", "10"], ["ADD", "a", "x"]])  # note
# next call
f([["ADD", "c", "y"]])

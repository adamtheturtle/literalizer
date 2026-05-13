module [result]

make_widget : a -> {}
make_widget = \_ -> {}
Val : [
    RInt I128,
]

result : Val
result = make_widget (RInt 42i128)

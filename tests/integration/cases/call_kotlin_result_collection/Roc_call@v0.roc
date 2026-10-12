module [my_data]

make_widget : a -> {}
make_widget = \_ -> {}

my_data = make_widget (RList [RList [RInt 1i128, RInt 2i128], RList [RInt 3i128]])

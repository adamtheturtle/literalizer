defmodule Check do
  def process(_value, _count), do: nil
  def x do
    my_int = 1
    my_bool = true
    my_float = 3.14
    my_list = [
        1,
        2,
        3,
    ]
    process(my_int, 42)
    process(my_bool, 7)
    process(my_float, 9)
    process(my_list, 1)
  end
end

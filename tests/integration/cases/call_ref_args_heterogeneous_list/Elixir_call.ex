defmodule Check do
  def process(_data, _count), do: nil
  def x do
    my_ints = [
        1,
        2,
        3,
    ]
    my_strings = [
        "a",
        "b",
    ]
    my_empty = []
    process(my_ints, 42)
    process(my_strings, 7)
    process(my_empty, 99)
  end
end

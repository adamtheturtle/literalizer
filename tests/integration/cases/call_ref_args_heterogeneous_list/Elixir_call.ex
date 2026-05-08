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
    process(my_ints, 42)
    process(my_strings, 7)
  end
end

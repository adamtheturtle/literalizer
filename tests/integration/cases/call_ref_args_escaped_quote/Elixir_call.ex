defmodule Check do
  def process(_v), do: nil
  def x do
    my_str = "a\"b"
    process(my_str)
  end
end

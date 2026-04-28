defmodule Check do
  def process(_data), do: nil
  def x do
    my_var = [
        1,
        2,
        3,
    ]
    process(my_var)
  end
end

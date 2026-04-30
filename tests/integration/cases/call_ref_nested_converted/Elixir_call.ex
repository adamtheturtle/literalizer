defmodule Check do
  def process(_data), do: nil
  def x do
    my_var = 42
    process([my_var, 42, "static"])
  end
end

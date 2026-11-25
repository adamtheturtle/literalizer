defmodule Check do
  def process(_value), do: nil
  def x do
    process(-1)
    process(-2)
    process(-3)
  end
end

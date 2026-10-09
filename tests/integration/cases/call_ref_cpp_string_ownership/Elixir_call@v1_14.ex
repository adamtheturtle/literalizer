defmodule Check do
  def consume(_value), do: nil
  def x do
    item = "s"
    consume(item)
  end
end

defmodule Check do
  def consume(_value), do: nil
  def x do
    item = [
        1,
        2,
    ]
    consume(item)
  end
end

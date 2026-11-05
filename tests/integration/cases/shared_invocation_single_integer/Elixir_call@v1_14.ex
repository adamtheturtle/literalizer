defmodule Check do
  def consume(_value), do: nil
  def x do
    consume(1)
  end
end

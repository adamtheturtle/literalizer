defmodule Check do
  def consume(_value), do: nil
  def x do
    shared = 42
    consume(shared)
  end
end

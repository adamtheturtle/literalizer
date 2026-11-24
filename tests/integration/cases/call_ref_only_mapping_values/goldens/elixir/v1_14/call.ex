defmodule Check do
  def consume(_value), do: nil
  def x do
    item = 42
    consume(%{"field" => item})
  end
end

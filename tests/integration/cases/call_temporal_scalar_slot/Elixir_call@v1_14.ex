defmodule Check do
  def process(_value), do: nil
  def x do
    process("09:30:00")
    process("2024-01-15T00:00:00+00:00")
    process(1)
  end
end

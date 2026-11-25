defmodule Check do
  def process(_value), do: nil
  def x do
    process("time.Date(2024, time.January, 15, 12, 0, 0, 0, time.UTC)")
  end
end

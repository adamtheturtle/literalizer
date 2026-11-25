defmodule Check do
  def process(_value), do: nil
  def x do
    process("hello")
    process(42)
    process(true)
  end
end

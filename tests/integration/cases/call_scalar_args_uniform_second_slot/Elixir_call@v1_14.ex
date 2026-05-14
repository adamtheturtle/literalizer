defmodule Check do
  def process(_value, _label), do: nil
  def x do
    process("hello", "a")
    process(42, "b")
    process(true, "c")
  end
end

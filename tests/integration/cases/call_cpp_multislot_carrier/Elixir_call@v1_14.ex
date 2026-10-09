defmodule Check do
  def process(_value, _extra), do: nil
  def x do
    process(1, "hello")
    process("two", false)
    process(3.5, nil)
  end
end

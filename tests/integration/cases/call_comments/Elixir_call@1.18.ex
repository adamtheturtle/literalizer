defmodule Check do
  def process(_value), do: nil
  def x do
    # Test cases
    process("hello")  # single word
    process("hello world")  # two words
    # trailing comment
  end
end

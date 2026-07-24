defmodule Check do
  def process(_value), do: nil
  def emit(_call, _zip), do: nil
  def x do
    emit(process("hello"), "one")
    emit(process(42), "zero")
  end
end

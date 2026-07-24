defmodule Check do
  def process(_value), do: nil
  def emit(_call, _zip), do: nil
  def x do
    emit(process("hello"), 1)
    emit(process(42), 0)
  end
end

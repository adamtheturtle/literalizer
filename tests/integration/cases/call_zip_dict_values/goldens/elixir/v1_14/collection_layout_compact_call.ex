defmodule Check do
  def process(_value), do: nil
  def emit(_call, _zip), do: nil
  def x do
    emit(process("hello"), %{"a" => 1, "b" => 2})
    emit(process(42), %{"c" => 3, "d" => 4})
  end
end

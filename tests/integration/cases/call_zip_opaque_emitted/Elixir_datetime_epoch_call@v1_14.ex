defmodule Check do
  def process(_value), do: nil
  def emit(_call, _zip), do: nil
  def x do
    emit(process(1), 1705320000)
  end
end

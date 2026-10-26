defmodule Check do
  def process(_value), do: nil
  def emit(_call, _zip), do: nil
  def x do
    emit(process(1), ~D[2024-01-15])
  end
end

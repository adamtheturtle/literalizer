defmodule Check do
  def process(_value), do: nil
  def emit(_call, _zip), do: nil
  def x do
    emit(process(1), ~N[2024-01-15 12:00:00])
  end
end

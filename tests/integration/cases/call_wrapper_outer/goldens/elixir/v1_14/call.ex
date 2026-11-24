defmodule Check do
  def process(_value), do: nil
  def emit(_arg), do: nil
  def x do
    emit(process(42))
  end
end

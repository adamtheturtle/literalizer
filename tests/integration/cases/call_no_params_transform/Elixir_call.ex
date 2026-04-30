defmodule Check do
  def process(), do: nil
  def emit(_arg), do: nil
  def x do
    emit(process())
    emit(process())
  end
end

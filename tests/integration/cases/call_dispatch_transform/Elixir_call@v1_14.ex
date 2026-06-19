defmodule Check do
  def record_value(_value), do: nil
  def flush_buffer(_count), do: nil
  def emit(_arg), do: nil
  def x do
    emit(record_value(42))
    flush_buffer(3)
  end
end

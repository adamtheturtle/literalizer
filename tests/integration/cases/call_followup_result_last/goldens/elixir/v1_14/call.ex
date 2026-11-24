defmodule Check do
  def make_widget(_first, _second), do: nil
  def consume(_first, _second), do: nil
  def x do
    my_data = make_widget(42, 3)
    consume(3, my_data)
  end
end

defmodule Check do
  def make_widget(_value), do: nil
  def consume(_value), do: nil
  def x do
    my_data = make_widget(42)
    consume(my_data)
  end
end

defmodule Check do
  def consume_widget(_arg), do: nil
  def x do
    item = nil
    my_data = nil
    consume_widget(my_data)
    my_data = item
    consume_widget(my_data)
  end
end

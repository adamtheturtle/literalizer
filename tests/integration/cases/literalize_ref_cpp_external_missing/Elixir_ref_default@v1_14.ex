defmodule Check do
  def consume_widget(_arg), do: nil
  def x do
    item = [
        1,
        2,
    ]
    my_data = [
        1,
        2,
    ]
    consume_widget(my_data)
    my_data = item
    consume_widget(my_data)
  end
end

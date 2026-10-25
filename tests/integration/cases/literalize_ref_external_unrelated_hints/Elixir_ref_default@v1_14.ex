defmodule Check do
  def consume_widget(_arg_value), do: nil
  def x do
    missing = [
        1,
        2,
    ]
    my_data = missing
    consume_widget(my_data)
  end
end

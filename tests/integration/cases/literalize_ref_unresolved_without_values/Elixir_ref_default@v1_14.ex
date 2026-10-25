defmodule Check do
  def consume_widget(_arg_value), do: nil
  def x do
    a = 0
    my_data = [
        a,
        1,
    ]
    consume_widget(my_data)
  end
end

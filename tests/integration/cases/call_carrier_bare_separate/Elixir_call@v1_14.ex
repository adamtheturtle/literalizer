defmodule Check do
  def make_widget(_first_value, _second_value), do: nil
  def x do
    make_widget([1], ["text"])
  end
end

defmodule Check do
  def process(_data), do: nil
  def x do
    my_list = []
    process([[%{"inner" => my_list}]])
  end
end

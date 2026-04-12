defmodule Check do
  def x do
    process(value: "hello")
    process(value: 42)
    process(value: true)
    _ = my_data
  end
end

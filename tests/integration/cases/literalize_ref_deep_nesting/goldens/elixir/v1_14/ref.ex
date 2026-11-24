defmodule Check do
  def x do
    deep = [
        [
            "one",
            "two",
        ],
        [
            "three",
            "four",
        ],
    ]
    my_data = %{
        "a" => %{
            "b" => %{
                "c" => deep,
            },
        },
    }
    _ = my_data
  end
end

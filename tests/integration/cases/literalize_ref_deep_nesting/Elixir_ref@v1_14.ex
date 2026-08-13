defmodule Check do
  def x do
    deep = [
        [
            1,
            2,
        ],
        [
            3,
            4,
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

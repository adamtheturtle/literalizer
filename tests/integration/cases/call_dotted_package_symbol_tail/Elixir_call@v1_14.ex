defmodule HelperType_ do
  def list(_a), do: nil
end
defmodule Check do
  def x do
    helper = HelperType_
    helper.list(1)
  end
end

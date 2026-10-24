defmodule ClassType_ do
  def member(_a), do: nil
end
defmodule Check do
  def x do
    class = ClassType_
    class.member(42)
  end
end

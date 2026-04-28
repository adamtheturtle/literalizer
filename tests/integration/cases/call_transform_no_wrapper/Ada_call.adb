with A_Stub; use A_Stub;
procedure Main is
    function Process (Value : A_Val) return A_Val is (ANull);
begin
    process(value => "hello");
    process(value => 42);
    process(value => ABool (True));
end Main;

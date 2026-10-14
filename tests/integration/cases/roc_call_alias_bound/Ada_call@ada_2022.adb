with A_Stub; use A_Stub;
procedure Main is
    function Process (Value : A_Val) return A_Val is (ANull);
    my_data : A_Val := Process(value => AInt (1));
begin
    null;
end Main;

with A_Stub; use A_Stub;
procedure Main is
    function Process (A : A_Val; B : A_Val) return A_Val is (ANull);
    my_data : A_Val := Process(a => AInt (1), b => AInt (2));
begin
    null;
end Main;

with A_Stub; use A_Stub;
procedure Main is
    function F (A : A_Val) return A_Val is (ANull);
    x : A_Val := AInt (1);
begin
    F(a => x);
end Main;

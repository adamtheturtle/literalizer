with A_Stub; use A_Stub;
procedure Main is
    function F (A : A_Val) return A_Val is (ANull);
    ref_data : A_Val := AInt (1);
begin
    F(a => ref_data);
end Main;

with A_Stub; use A_Stub;
procedure Main is
    function F (A : A_Val) return A_Val is (ANull);
    procedure Repr (Argument0 : A_Val) is begin null; end Repr;
    ref_data : A_Val := AInt (1);
begin
    Repr(argument0 => F(a => ref_data));
end Main;

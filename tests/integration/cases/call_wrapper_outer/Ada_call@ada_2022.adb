with A_Stub; use A_Stub;
procedure Main is
    function Process (Value : A_Val) return A_Val is (ANull);
    procedure Emit (Argument0 : A_Val) is begin null; end Emit;
begin
    Emit(argument0 => Process(value => AInt (42)));
end Main;

with A_Stub; use A_Stub;
procedure Main is
    function Process (Value : A_Val) return A_Val is (ANull);
    procedure Emit (Argument0 : A_Val; Argument1 : A_Val) is begin null; end Emit;
begin
    Emit(argument0 => Process(value => AStr ("hello")), argument1 => ABool (True));
    Emit(argument0 => Process(value => AInt (42)), argument1 => ABool (False));
end Main;

with A_Stub; use A_Stub;
procedure Main is
    function Process (Value : A_Val) return A_Val is (ANull);
    procedure Emit (Call : A_Val; Zip : A_Val) is begin null; end Emit;
begin
    emit(Process(value => AInt (42)), AStr ("one"));
end Main;

with A_Stub; use A_Stub;
procedure Main is
    function Process (Value : A_Val) return A_Val is (ANull);
    procedure Emit (Call : A_Val; Zip : A_Val) is begin null; end Emit;
begin
    emit(Process(value => AStr ("hello")), AMap'[AEntry ("a", AInt (1)), AEntry ("b", AInt (2))]);
    emit(Process(value => AInt (42)), AMap'[AEntry ("c", AInt (3)), AEntry ("d", AInt (4))]);
end Main;

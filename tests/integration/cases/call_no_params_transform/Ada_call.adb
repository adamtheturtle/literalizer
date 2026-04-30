with A_Stub; use A_Stub;
procedure Main is
    function Process return A_Val is (ANull);
    procedure Emit (Arg : A_Val) is begin null; end Emit;
begin
    emit(Process());
    emit(Process());
end Main;

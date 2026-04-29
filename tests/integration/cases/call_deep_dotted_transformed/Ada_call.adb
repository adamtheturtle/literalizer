with A_Stub; use A_Stub;
procedure Main is
    function Fetch (Payload : A_Val) return A_Val is (ANull);
    procedure Emit (Arg : A_Val) is begin null; end Emit;
begin
    emit(Fetch(payload => AStr ("hello")));
    emit(Fetch(payload => AInt (42)));
    emit(Fetch(payload => ABool (True)));
end Main;

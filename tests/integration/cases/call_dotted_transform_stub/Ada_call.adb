with A_Stub; use A_Stub;
procedure Main is
    function Process (Value : A_Val) return A_Val is (ANull);
    procedure Emit (Arg : A_Val) is begin null; end Emit;
begin
    tracer.emit(Process(value => AStr ("hello")));
    tracer.emit(Process(value => AInt (42)));
    tracer.emit(Process(value => ABool (True)));
end Main;

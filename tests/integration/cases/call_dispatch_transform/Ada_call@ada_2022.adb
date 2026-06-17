with A_Stub; use A_Stub;
procedure Main is
    function Record_Value (Value : A_Val) return A_Val is (ANull);
    procedure Flush_Buffer (Count : A_Val) is begin null; end Flush_Buffer;
    procedure Emit (Arg : A_Val) is begin null; end Emit;
begin
    emit(Record_Value(value => AInt (42)));
    Flush_Buffer(count => AInt (3));
end Main;

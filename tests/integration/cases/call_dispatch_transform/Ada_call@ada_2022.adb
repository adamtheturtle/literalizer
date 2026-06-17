with A_Stub; use A_Stub;
procedure Main is
    function Record (Value : A_Val) return A_Val is (ANull);
    procedure Flush (Count : A_Val) is begin null; end Flush;
begin
    Record(value => AInt (42));
    Flush(count => AInt (3));
end Main;

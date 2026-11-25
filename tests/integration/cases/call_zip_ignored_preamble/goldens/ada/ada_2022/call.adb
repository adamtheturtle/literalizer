with A_Stub; use A_Stub;
procedure Main is
    function Process (Value : A_Val) return A_Val is (ANull);
begin
    declare
        Discarded_Value : constant A_Val := Process(value => AInt (1));
        pragma Unreferenced (Discarded_Value);
    begin
        null;
    end;
    declare
        Discarded_Value : constant A_Val := Process(value => AInt (2));
        pragma Unreferenced (Discarded_Value);
    begin
        null;
    end;
end Main;

with A_Stub; use A_Stub;
procedure Main is
    function Process (Value : A_Val) return A_Val is (ANull);
begin
    declare
        Discarded_Value : constant A_Val := Process(value => AStr ("time.Date(2024, time.January, 15, 12, 0, 0, 0, time.UTC)"));
        pragma Unreferenced (Discarded_Value);
    begin
        null;
    end;
end Main;

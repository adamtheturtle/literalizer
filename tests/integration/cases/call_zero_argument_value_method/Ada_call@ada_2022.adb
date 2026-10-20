with A_Stub; use A_Stub;
procedure Main is
    function Go return A_Val is (ANull);
begin
    declare
        Discarded_Value : constant A_Val := Go;
        pragma Unreferenced (Discarded_Value);
    begin
        null;
    end;
end Main;

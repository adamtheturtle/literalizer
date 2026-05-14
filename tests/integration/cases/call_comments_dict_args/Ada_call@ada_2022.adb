with A_Stub; use A_Stub;
procedure Main is
    procedure Process (Value : A_Val) is begin null; end Process;
begin
    -- Test cases
    Process(value => AMap'[AEntry ("type", AStr ("create")), AEntry ("pr_id", AStr ("pr_1"))]);  -- first case
    Process(value => AMap'[AEntry ("type", AStr ("update")), AEntry ("pr_id", AStr ("pr_2"))]);  -- second case
    -- third case
    Process(value => AMap'[AEntry ("type", AStr ("delete")), AEntry ("pr_id", AStr ("pr_3"))]);
end Main;

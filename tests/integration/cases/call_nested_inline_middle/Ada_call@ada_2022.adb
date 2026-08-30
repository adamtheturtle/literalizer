with A_Stub; use A_Stub;
procedure Main is
    procedure F (Ops : A_Val) is begin null; end F;
begin
    F(ops => AList'[AList'[AStr ("DEL"), AStr ("b"), AStr ("10")], AList'[AStr ("ADD"), AStr ("a"), AStr ("x")]]);  -- note
    -- next call
    F(ops => AList'[AList'[AStr ("ADD"), AStr ("c"), AStr ("y")]]);
end Main;

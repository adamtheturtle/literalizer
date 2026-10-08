with A_Stub; use A_Stub;
procedure Main is
    procedure Process (Value : A_Val) is begin null; end Process;
begin
    Process(value => AInt (1));  -- note<U+2028>still commented<U+2029>done
end Main;

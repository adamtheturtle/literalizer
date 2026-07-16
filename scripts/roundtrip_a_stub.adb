--  See ``roundtrip_a_stub.ads`` for the design notes.

with Ada.Strings.Unbounded;     use Ada.Strings.Unbounded;
with GNATCOLL.JSON;             use GNATCOLL.JSON;

package body A_Stub is

   function Empty return A_Val is
   begin
      return (Data => new Payload'(Kind => List_K, Items => <>));
   end Empty;

   procedure Append (Container : in out A_Val; Item : A_Val) is
   begin
      if Container.Data = null then
         Container.Data := new Payload'(Kind => List_K, Items => <>);
      end if;
      --  Promote a freshly-emptied container to a map the first time
      --  an ``AEntry`` arrives; subsequent items stay in whichever
      --  variant the first item established.
      if Item.Data /= null
        and then Item.Data.Kind = Entry_K
        and then Container.Data.Kind = List_K
        and then Container.Data.Items.Is_Empty
      then
         Container.Data := new Payload'(Kind => Map_K, Items => <>);
      end if;
      Container.Data.Items.Append (Item);
   end Append;

   function AStr (S : String) return A_Val is
   begin
      return (Data => new Payload'(Kind  => Str_K,
                                   Str_V => To_Unbounded_String (S)));
   end AStr;

   function AInt (I : Long_Long_Integer) return A_Val is
   begin
      return (Data => new Payload'(Kind => Int_K, Int_V => I));
   end AInt;

   function AFloat (F : Long_Float) return A_Val is
   begin
      return (Data => new Payload'(Kind => Float_K, Float_V => F));
   end AFloat;

   function ABool (B : Boolean) return A_Val is
   begin
      return (Data => new Payload'(Kind => Bool_K, Bool_V => B));
   end ABool;

   function AEntry (Key : String; Value : A_Val) return A_Val is
   begin
      return (Data => new Payload'
                (Kind      => Entry_K,
                 Entry_Key => To_Unbounded_String (Key),
                 Entry_Val => Value));
   end AEntry;

   --  Translate an ``A_Val`` tree to a ``GNATCOLL.JSON.JSON_Value`` so
   --  ``GNATCOLL.JSON.Write`` can do the string escaping and number
   --  formatting.  ``Entry_K`` should only appear as an immediate
   --  child of a ``Map_K`` (the ``Map_K`` arm consumes it inline); it
   --  cannot appear at the top level of the round-trip input.
   function To_JSON_Value (V : A_Val) return JSON_Value is
   begin
      if V.Data = null then
         return Create;
      end if;
      case V.Data.Kind is
         when Null_K =>
            return Create;
         when Bool_K =>
            return Create (V.Data.Bool_V);
         when Int_K =>
            return Create (V.Data.Int_V);
         when Float_K =>
            return Create (V.Data.Float_V);
         when Str_K =>
            return Create (To_String (V.Data.Str_V));
         when Entry_K =>
            raise Program_Error
              with "AEntry outside of a map";
         when List_K =>
            declare
               Arr : JSON_Array := Empty_Array;
            begin
               for Child of V.Data.Items loop
                  Append (Arr, To_JSON_Value (Child));
               end loop;
               return Create (Arr);
            end;
         when Map_K =>
            declare
               Obj : constant JSON_Value := Create_Object;
            begin
               for Child of V.Data.Items loop
                  Set_Field
                    (Obj,
                     To_String (Child.Data.Entry_Key),
                     To_JSON_Value (Child.Data.Entry_Val));
               end loop;
               return Obj;
            end;
      end case;
   end To_JSON_Value;

   function To_JSON (V : A_Val) return String is
   begin
      return Write (To_JSON_Value (V), Compact => True);
   end To_JSON;

end A_Stub;

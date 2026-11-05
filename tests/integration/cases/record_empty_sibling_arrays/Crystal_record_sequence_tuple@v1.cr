module Fixture_record_empty_sibling_arrays_Crystal_record_sequence_tuple
extend self
record Record1, item : Int32
record Record2, item : Nil
record Record0, integers : Tuple(Tuple(), Tuple(Record1)), nulls : Tuple(Tuple(), Tuple(Record2)), nested : Tuple(Tuple(Tuple(), Tuple(Record1)), Tuple(Tuple(Record1), Tuple())), reversed : Tuple(Tuple(Record1), Tuple())
my_data = Record0.new(
    {
        Tuple.new,
         {
            Record1.new(
                1,
            ),
        },
    },
    {
        Tuple.new,
         {
            Record2.new(
                nil,
            ),
        },
    },
    {
         {
            Tuple.new,
             {
                Record1.new(
                    2,
                ),
            },
        },
         {
             {
                Record1.new(
                    3,
                ),
            },
            Tuple.new,
        },
    },
    {
         {
            Record1.new(
                4,
            ),
        },
        Tuple.new,
    },
)
end

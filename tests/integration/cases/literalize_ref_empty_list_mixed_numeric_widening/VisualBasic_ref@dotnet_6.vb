Imports System.Collections.Generic
Module Check
    Dim EmptyValues = New Object() {}
    Dim IntegerValues = New Integer() {
        1
    }
    Dim FloatValues = New Double() {
        1.5
    }
    Dim my_data = New Double()() {
        EmptyValues,
        IntegerValues,
        FloatValues
    }
End Module

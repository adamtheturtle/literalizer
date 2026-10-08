Imports System.Collections.Generic
Module Check
    Dim Actual = 42
    Dim my_data = New Object() {
        New Dictionary(Of String, Object) From {{"$ref", 1}},
        New Dictionary(Of String, Object) From {{"$ref", Nothing}},
        Actual
    }
End Module

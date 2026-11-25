Imports System.Collections.Generic
Module Check
    Dim my_data = New Dictionary(Of String, Object) From {
        {"value", New Dictionary(Of String, Object) From {{"$ref", "foo"}}}
    }
End Module

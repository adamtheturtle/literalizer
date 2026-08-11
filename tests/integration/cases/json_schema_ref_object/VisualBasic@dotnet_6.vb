Imports System.Collections.Generic
Module Check
    Dim my_data = New Dictionary(Of String, Object) From {
        {"schema", New Dictionary(Of String, Object) From {{"$ref", "#/defs/Foo"}}}
    }
End Module

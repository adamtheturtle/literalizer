Imports System.Collections.Generic
Module Check
    Dim Foo = New Dictionary(Of String, Object) From {
        {"_", "_"}
    }
    Dim my_data = New Dictionary(Of String, Object) From {
        {"mapping", New Dictionary(Of String, Object) From {{"value", Foo}}},
        {"items", New Object() {New Dictionary(Of String, Object) From {{"other", 1}}, Foo}}
    }
End Module

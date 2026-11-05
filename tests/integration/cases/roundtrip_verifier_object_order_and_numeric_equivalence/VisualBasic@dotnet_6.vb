Imports System.Collections.Generic
Module Check
    Dim my_data = New Dictionary(Of String, Object) From {
        {"b", Nothing},
        {"a", New Dictionary(Of String, Object) From {{"y", New Double() {1.0}}, {"x", False}}}
    }
End Module

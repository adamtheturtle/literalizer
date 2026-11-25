Imports System.Collections.Generic
Module Check
    Dim my_data = New Dictionary(Of String, Object) From {
        {"h", New Object() {1, "a", New Object() {2, "b"}, New Dictionary(Of String, Object) From {{"k", New Boolean() {True}}}}}
    }
End Module

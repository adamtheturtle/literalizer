Imports System.Collections.Generic
Module Check
    Dim my_data = New Dictionary(Of String, Object) From {
        {"nil", New Object() {New Object() {New Object() {New Object() {New Object() {New Object() {New Object() {New Object() {New Object() {Nothing}}}}}}}}}},
        {"empty", New Object() {New Object() {New Object() {New Object() {New Object() {New Object() {New Object() {New Object() {New Object() {New Object() {}}}}}}}}}}},
        {"siblings", New Object() {New Object() {New Integer()()()()()()()() {New Integer()()()()()()() {New Integer()()()()()() {New Integer()()()()() {New Integer()()()() {New Integer()()() {New Integer()() {New Integer() {4, 5}}}}}}}}}}}
    }
End Module

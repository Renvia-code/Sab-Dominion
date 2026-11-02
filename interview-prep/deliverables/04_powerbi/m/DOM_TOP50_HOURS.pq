// Query DOM_TOP50_HOURS (Import)
let
    Source = Csv.Document(File.Contents(DataFolder & "dom_top50_hours.csv"), [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]),
    Promoted = Table.PromoteHeaders(Source, [PromoteAllScalars = true]),
    UpperNames = Table.TransformColumnNames(Promoted, Text.Upper),
    Selected = Table.SelectColumns(UpperNames, {"YEAR", "DATA_DATE", "HOUR_NO", "UTC_TS", "DEMAND_MW", "RANK_TODAY", "RANK_END_2025"}),
    Blanks = Table.ReplaceValue(Selected, "", null, Replacer.ReplaceValue, Table.ColumnNames(Selected)),
    Typed = Table.TransformColumnTypes(Blanks, {{"YEAR", type number}, {"DATA_DATE", type datetime}, {"HOUR_NO", type number}, {"UTC_TS", type datetime}, {"DEMAND_MW", type number}, {"RANK_TODAY", type number}, {"RANK_END_2025", type number}}, "en-US")
in
    Typed

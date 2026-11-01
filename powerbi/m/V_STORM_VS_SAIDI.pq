// Query V_STORM_VS_SAIDI (Import)
let
    Source = Csv.Document(File.Contents(DataFolder & "storm_vs_saidi.csv"), [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]),
    Promoted = Table.PromoteHeaders(Source, [PromoteAllScalars = true]),
    UpperNames = Table.TransformColumnNames(Promoted, Text.Upper),
    Selected = Table.SelectColumns(UpperNames, {"YEAR", "STORM_COUNTY_DAYS", "WIND_DAYS", "WINTER_DAYS", "TROPICAL_DAYS", "SAIDI_EX_MED", "SAIFI_EX_MED", "STORM_SAIDI", "SEVERE_GUST_DAYS"}),
    Blanks = Table.ReplaceValue(Selected, "", null, Replacer.ReplaceValue, Table.ColumnNames(Selected)),
    Typed = Table.TransformColumnTypes(Blanks, {{"YEAR", type number}, {"STORM_COUNTY_DAYS", type number}, {"WIND_DAYS", type number}, {"WINTER_DAYS", type number}, {"TROPICAL_DAYS", type number}, {"SAIDI_EX_MED", type number}, {"SAIFI_EX_MED", type number}, {"STORM_SAIDI", type number}, {"SEVERE_GUST_DAYS", type number}}, "en-US")
in
    Typed

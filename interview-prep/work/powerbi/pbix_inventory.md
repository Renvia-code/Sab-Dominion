# Report inventory: `original_copy_readonly.pbix` (read-only decode)

## report.json

```json
{
 "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/report/3.3.0/schema.json",
 "themeCollection": {
  "baseTheme": {
   "name": "Fluent2-CY26SU10",
   "reportVersionAtImport": {
    "visual": "2.14.0",
    "report": "3.4.0",
    "page": "2.3.1"
   },
   "type": "SharedResources"
  }
 },
 "objects": {
  "section": [
   {
    "properties": {
     "verticalAlignment": {
      "expr": {
       "Literal": {
        "Value": "'Top'"
       }
      }
     }
    }
   }
  ],
  "outspacePane": [
   {
    "properties": {
     "expanded": {
      "expr": {
       "Literal": {
        "Value": "true"
       }
      }
     }
    }
   }
  ]
 },
 "resourcePackages": [
  {
   "name": "SharedResources",
   "type": "SharedResources",
   "items": [
    {
     "name": "Fluent2-CY26SU10",
     "path": "BaseThemes/Fluent2-CY26SU10.json",
     "type": "BaseTheme"
    }
   ]
  }
 ],
 "settings": {
  "useStylableVisualContainerHeader": true,
  "exportDataMode": "AllowSummarized",
  "defaultDrillFilterOtherVisuals": true,
  "allowChangeFilterTypes": true,
  "useEnhancedTooltips": true,
  "useDefaultAggregateDisplayName": true
 }
}
```

## Page `61745dccdb7948ee4977`: "Scorecards" (1920x1080)

Page filters: `{"filters": [{"name": "741ccac639ab0e208f89", "field": {"Column": {"Expression": {"SourceRef": {"Entity": "DIM_UTILITY"}}, "Property": "PEER_GROUP"}}, "type": "Categorical", "filter": {"Version": 2, "From": [{"Name": "d", "Entity": "DIM_UTILITY", "Type": 0}], "Where": [{"Condition": {"In": {"Expressions": [{"Column": {"Expression": {"SourceRef": {"Source": "d"}}, "Property": "PEER_GROUP"}}], "Values": [[{"Literal": {"Value": "'Dominion Energy Virginia'"}}]]}}}]}, "howCreated": "User"}, {"name": "16bbffbcb33f6543413e", "field": {"Column": {"Expression": {"SourceRef": {"Entity": "FCT_RELIABILITY`

- **cardVisual** `1b4422116d6104d407dd` at x=11 y=632 w=265 h=149
  - alt text: none
  - Data: [Top 50 hours in 2025] (measure on DOM_TOP50_HOURS)
- **cardVisual** `268053916982bec30f81` at x=1333 y=0 w=367 h=122
  - alt text: none
  - Data: [Share of outage mins caused by major storms] (measure on FCT_RELIABILITY)
- **cardVisual** `2bddd35670236987c7c1` at x=10 y=0 w=201 h=121
  - alt text: none
  - Data: [SAIDI ex MED] (measure on FCT_RELIABILITY)
  - visual filters: `{"filters": [{"name": "2759ff83cbae349a0a6d", "field": {"Measure": {"Expression": {"SourceRef": {"Entity": "FCT_RELIABILITY"}}, "Property": "SAIDI ex MED"}}, "type": "Advanced"}]}`
- **cardVisual** `3bc57cca3f71ef9d7cc3` at x=438 y=0 w=221 h=122
  - alt text: none
  - Data: [SAIFI ex MED] (measure on FCT_RELIABILITY)
  - visual filters: `{"filters": [{"name": "be554f44989ea5986de0", "field": {"Measure": {"Expression": {"SourceRef": {"Entity": "FCT_RELIABILITY"}}, "Property": "SAIFI ex MED"}}, "type": "Advanced"}]}`
- **cardVisual** `4815afead0c6a4a7ca4b` at x=211 y=0 w=226 h=122
  - alt text: none
  - Data: Sum of FCT_RELIABILITY[Customers Served]
- **cardVisual** `588c5e9877c5c13562f4` at x=945 y=0 w=388 h=122
  - alt text: none
  - Data: [SAIDI all events] (measure on FCT_RELIABILITY)
  - visual filters: `{"filters": [{"name": "efc207c99dc5209bca75", "field": {"Measure": {"Expression": {"SourceRef": {"Entity": "FCT_RELIABILITY"}}, "Property": "SAIDI all events"}}, "type": "Advanced"}]}`
- **cardVisual** `7a8692e79a615d758900` at x=659 y=0 w=287 h=122
  - alt text: none
  - Data: [CAIDI ex MED] (measure on FCT_RELIABILITY)
  - visual filters: `{"filters": [{"name": "87c4ed62b09072ddc705", "field": {"Measure": {"Expression": {"SourceRef": {"Entity": "FCT_RELIABILITY"}}, "Property": "CAIDI ex MED"}}, "type": "Advanced"}]}`
- **cardVisual** `ca269581fd1be8142455` at x=10 y=201 w=230 h=150
  - alt text: none
  - Data: [Floor growth 2019 to 2025] (measure on DOM_LOAD_ANNUAL)
- **cardVisual** `ea221bd41bd7ea9c1c49` at x=10 y=416 w=230 h=150
  - alt text: none
  - Data: [Peak growth 2019 to 2025] (measure on DOM_LOAD_ANNUAL)

## Page `2414a423c3820b09c17c`: "What Moved" (1920x1080)

Page filters: `{"filters": [{"name": "27946d8a96078ee02987", "field": {"Column": {"Expression": {"SourceRef": {"Entity": "DIM_UTILITY"}}, "Property": "PEER_GROUP"}}, "type": "Categorical", "filter": {"Version": 2, "From": [{"Name": "d", "Entity": "DIM_UTILITY", "Type": 0}], "Where": [{"Condition": {"In": {"Expressions": [{"Column": {"Expression": {"SourceRef": {"Source": "d"}}, "Property": "PEER_GROUP"}}], "Values": [[{"Literal": {"Value": "'Dominion Energy Virginia'"}}]]}}}]}, "howCreated": "User"}]}`

- **lineChart** `a56e85d260bd5432b881` at x=676 y=518 w=1042 h=489
  - title/text: "Minutes to restore each outage down 9% since 2019"
  - subtitle: "CAIDI, excluding major event days. Dominion Energy Virginia, EIA-861 | axis valueAxis: "Minutes Per Outage""
  - alt text: none
  - Category: FCT_RELIABILITY[YEAR] (column)
  - Y: [CAIDI ex MED] (measure on FCT_RELIABILITY)
- **lineChart** `eb9e34101c7ddbafa3ba` at x=11 y=0 w=1089 h=489
  - title/text: "Outages per customer up 6% since 2019, most of it after 2023"
  - subtitle: "SAIFI, excluding major event days. Dominion Energy Virginia, EIA-861 | axis valueAxis: "Outages per Customer per Year""
  - alt text: none
  - Category: FCT_RELIABILITY[YEAR] (column)
  - Y: Sum of FCT_RELIABILITY[SAIFI_EX_MED]

## Page `241c63d8c7e81067e9cc`: "Weather" (1920x1080)

Page filters: `{"filters": [{"name": "412efad00a2b71a9c18b", "field": {"Column": {"Expression": {"SourceRef": {"Entity": "DIM_UTILITY"}}, "Property": "PEER_GROUP"}}, "type": "Categorical", "filter": {"Version": 2, "From": [{"Name": "d", "Entity": "DIM_UTILITY", "Type": 0}], "Where": [{"Condition": {"In": {"Expressions": [{"Column": {"Expression": {"SourceRef": {"Source": "d"}}, "Property": "PEER_GROUP"}}], "Values": [[{"Literal": {"Value": "'Dominion Energy Virginia'"}}]]}}}]}, "howCreated": "User"}]}`

- **lineChart** `0cdbc9919c3afef37960` at x=935 y=532 w=984 h=549
  - title/text: "Remove the weather and the underlying number has not moved since 2015"
  - subtitle: "SAIDI ex MED, actual vs weather-adjusted using the NOAA storm-day fit. Dominion Energy Virginia | axis valueAxis: "Outage Mins per Customer""
  - alt text: none
  - Category: SAIDI_WEATHER_ADJUSTED[YEAR] (column)
  - Y: Sum of SAIDI_WEATHER_ADJUSTED[SAIDI_EX_MED]
  - Y: Sum of SAIDI_WEATHER_ADJUSTED[WEATHER_ADJUSTED_SAIDI]
- **scatterChart** `cd3dca34756db97f5ed6` at x=1145 y=0 w=775 h=521
  - title/text: "More storm days, more outage minutes. 2025 sits where its weather predicts"
  - subtitle: "NOAA storm county-days in Dominion’s Virginia counties vs SAIDI ex MED, 2013 to 2025 | axis valueAxis: "Outage mins per customer"; categoryAxis: "Storm county-days (NOAA)""
  - alt text: none
  - Category: V_STORM_VS_SAIDI[YEAR] (column)
  - X: Sum of V_STORM_VS_SAIDI[STORM_COUNTY_DAYS]
  - Y: Sum of V_STORM_VS_SAIDI[SAIDI_EX_MED]
  - visual filters: `{"filters": [{"name": "a6aebe7ec05999051e36", "field": {"Column": {"Expression": {"SourceRef": {"Entity": "V_STORM_VS_SAIDI"}}, "Property": "YEAR"}}, "type": "Advanced"}, {"name": "d325dedea20b8eb647a9", "field": {"Aggregation": {"Expression": {"Column": {"Expression": {"SourceRef": {"Entity": "V_ST`
- **columnChart** `d2efd4d136e889ee2b0e` at x=10 y=0 w=1135 h=520
  - title/text: "Major storms are half of all outage minutes in 2025, and the whole of the bad years"
  - subtitle: "Minutes per customer, with and without major storm days. Dominion Energy Virginia, EIA-861 | axis valueAxis: "Outage Mins per Customer""
  - alt text: none
  - Category: FCT_RELIABILITY[YEAR] (column)
  - Y: [SAIDI ex MED] (measure on FCT_RELIABILITY)
  - Y: [Storm SAIDI] (measure on FCT_RELIABILITY)
  - visual filters: `{"filters": [{"name": "9dc7de81909969332470", "field": {"Column": {"Expression": {"SourceRef": {"Entity": "FCT_RELIABILITY"}}, "Property": "YEAR"}}, "type": "Advanced"}, {"name": "aca885cf70b06edacc00", "field": {"Measure": {"Expression": {"SourceRef": {"Entity": "FCT_RELIABILITY"}}, "Property": "SA`
- **lineChart** `dcda2b950535cd9fed73` at x=11 y=532 w=925 h=521
  - title/text: "Same storms, different outcome: co-op outage frequency up 37% since 2015, Dominion up 14%"
  - subtitle: "SAIFI ex MED, 2015 = 100. Dominion vs all Virginia co-ops. EIA-861"
  - alt text: none
  - Category: V_GROUP_INDEX[YEAR] (column)
  - Series: V_GROUP_INDEX[PEER_GROUP] (column)
  - Y: [SAIFI index 2015] (measure on V_GROUP_INDEX)
  - visual filters: `{"filters": [{"name": "2734ae860c3e601e026b", "field": {"Column": {"Expression": {"SourceRef": {"Entity": "V_GROUP_INDEX"}}, "Property": "PEER_GROUP"}}, "type": "Categorical", "filter": {"Version": 2, "From": [{"Name": "v", "Entity": "V_GROUP_INDEX", "Type": 0}], "Where": [{"Condition": {"In": {"Exp`

## Page `39dca24cb135da967227`: "Peer Comparision" (1920x1080)

Page filters: `{"filters": [{"name": "7d64c2d867bc4b72fc1f", "field": {"Column": {"Expression": {"SourceRef": {"Entity": "DIM_UTILITY"}}, "Property": "PEER_GROUP"}}, "type": "Categorical", "filter": {"Version": 2, "From": [{"Name": "d", "Entity": "DIM_UTILITY", "Type": 0}], "Where": [{"Condition": {"In": {"Expressions": [{"Column": {"Expression": {"SourceRef": {"Source": "d"}}, "Property": "PEER_GROUP"}}], "Values": [[{"Literal": {"Value": "'Dominion Energy Virginia'"}}], [{"Literal": {"Value": "'Florida IOU peer'"}}], [{"Literal": {"Value": "'Mid-Atlantic IOU peer'"}}], [{"Literal": {"Value": "'Southeast IO`

- **clusteredBarChart** `572942895d9e7db615ca` at x=0 y=0 w=1005 h=554
  - title/text: "Fourth-highest outage minutes of twelve large utilities, 2023 to 2025"
  - subtitle: "SAIDI ex MED, 3-year average. Dominion excludes storms by its own rule, most peers by IEEE 1366, so gaps are indicative | axis valueAxis: "Yearly Outage mins per Customer""
  - alt text: none
  - Category: DIM_UTILITY[Display name] (column)
  - Y: [SAIDI 2023 to 2025] (measure on FCT_RELIABILITY)
- **scatterChart** `99301c6283764dcfd28f` at x=1037 y=0 w=871 h=554
  - title/text: "Restoration time is mid-pack. Outage frequency is the gap"
  - subtitle: "5-year averages 2021 to 2025, excluding major event days | axis valueAxis: "Minutes to restore each outage (CAIDI)"; categoryAxis: "Yearly Outages per Customer (SAIFI)""
  - alt text: none
  - Category: DIM_UTILITY[Quadrant name] (column)
  - Series: DIM_UTILITY[Short name] (column)
  - X: [SAIFI 5yr] (measure on FCT_RELIABILITY)
  - Y: [CAIDI 5yr] (measure on FCT_RELIABILITY)
- **tableEx** `abfe0d2588105da0a784` at x=453 y=585 w=1038 h=434
  - alt text: none
  - Values: DIM_UTILITY[Display name] (column)
  - Values: DIM_UTILITY[Region] (column)
  - Values: [Method] (measure on FCT_RELIABILITY)
  - Values: [SAIDI 2015 to 2017] (measure on FCT_RELIABILITY)
  - Values: [SAIDI 2023 to 2025] (measure on FCT_RELIABILITY)
  - Values: [SAIDI change %] (measure on FCT_RELIABILITY)
  - Values: [CAIDI 5yr] (measure on FCT_RELIABILITY)

## Page `4348e5cd66c9b48126f0`: "Growth" (1920x1080)

- **clusteredBarChart** `1b2743b4ff761d5db85f` at x=9 y=525 w=951 h=518
  - title/text: "The meters are installed. Almost nobody is on a rate that uses them"
  - subtitle: "Share of customers with a smart meter vs share on a time-varying rate, 2025. EIA-861 | axis valueAxis: "Share %""
  - alt text: none
  - Category: Programmes2025[utility] (column)
  - Y: [Smart meter share %] (measure on Programmes2025)
  - Y: [Time-varying rate %] (measure on Programmes2025)
  - visual filters: `{"filters": [{"name": "13f57dd78583a62c8dcc", "field": {"Column": {"Expression": {"SourceRef": {"Entity": "Programmes2025"}}, "Property": "utility"}}, "type": "Categorical", "filter": {"Version": 2, "From": [{"Name": "p", "Entity": "Programmes2025", "Type": 0}], "Where": [{"Condition": {"Not": {"Exp`
- **lineChart** `3e0ddca78b79485a3fea` at x=9 y=0 w=951 h=516
  - title/text: "Commercial sales up 65% since 2013 on 8% more customers. That gap is data centres"
  - subtitle: "Retail sales and customer counts, 2013 = 100. Dominion Energy Virginia, EIA-861 | axis valueAxis: "Index, 2023 = 100""
  - alt text: none
  - Category: LoadGrowth[year] (column)
  - Y: Sum of LoadGrowth[commercial_sales_index]
  - Y: Sum of LoadGrowth[commercial_customers_index]
  - Y: Sum of LoadGrowth[residential_sales_index]
- **clusteredColumnChart** `7b0e71f981e225998e87` at x=960 y=9 w=950 h=516
  - title/text: "Load growth 2019 to 2025 by hour of day: night +41%, afternoon +27%"
  - subtitle: "Change in average demand for each hour of the day, PJM DOM zone, EIA-930 | axis valueAxis: "Growth %"; categoryAxis: "Hour of Day""
  - alt text: none
  - Category: DOM_LOAD_PROFILE[HOUR_NO] (column)
  - Y: Sum of DOM_LOAD_PROFILE[GROWTH_PCT]

## Page `e8d8451399dc68c3ece6`: "Seasonal" (1920x1080)

- **clusteredColumnChart** `e1c9d78e2ce3b1f88809` at x=81 y=135 w=992 h=500
  - title/text: "Winter peak now matches summer: higher in 2022, 2025 and 2026"
  - subtitle: "Highest hour in Dec to Feb vs Jun to Aug each year, PJM DOM zone, EIA-930. 2026 summer is complete, winter is Jan to Feb only | axis valueAxis: "Peak Demand, MW""
  - alt text: none
  - Category: DOM_LOAD_ANNUAL[YEAR] (column)
  - Y: [Winter peak MW] (measure on DOM_LOAD_ANNUAL)
  - Y: [Summer peak MW] (measure on DOM_LOAD_ANNUAL)
  - visual filters: `{"filters": [{"name": "f9ea788de356277992d6", "ordinal": 0, "field": {"Measure": {"Expression": {"SourceRef": {"Entity": "DOM_LOAD_ANNUAL"}}, "Property": "Summer peak MW"}}, "type": "Advanced"}, {"name": "c49ecb93430bfb2c2b29", "ordinal": 1, "field": {"Measure": {"Expression": {"SourceRef": {"Entity`

## Page `e6f27ff89680632d5471`: "Executive Dashboard-1" (1920x1080)

- **lineChart** `1bc8e4107099744b0737` at x=0 y=603 w=980 h=477
  - title/text: "Remove the weather and the underlying number has not moved since 2015"
  - subtitle: "SAIDI ex MED, actual vs weather-adjusted using the NOAA storm-day fit. Dominion Energy Virginia | axis valueAxis: "Outage Mins per Customer""
  - alt text: none
  - Category: SAIDI_WEATHER_ADJUSTED[YEAR] (column)
  - Y: Sum of SAIDI_WEATHER_ADJUSTED[SAIDI_EX_MED]
  - Y: Sum of SAIDI_WEATHER_ADJUSTED[WEATHER_ADJUSTED_SAIDI]
- **slicer** `56198e8c521b4d60a663` at x=680 y=10 w=300 h=69
  - alt text: none
  - Values: DIM_UTILITY[PEER_GROUP] (column)
  - visual filters: `{"filters": [{"name": "1ce4323fc2b6b5d00dcd", "field": {"Column": {"Expression": {"SourceRef": {"Entity": "DIM_UTILITY"}}, "Property": "PEER_GROUP"}}, "type": "Categorical"}]}`
- **lineChart** `5aedb895e782649461c9` at x=980 y=149 w=939 h=454
  - title/text: "Minutes to restore each outage down 9% since 2019"
  - subtitle: "CAIDI, excluding major event days. Dominion Energy Virginia, EIA-861 | axis valueAxis: "Minutes Per Outage""
  - alt text: none
  - Category: FCT_RELIABILITY[YEAR] (column)
  - Y: [CAIDI ex MED] (measure on FCT_RELIABILITY)
  - visual filters: `{"filters": [{"name": "fcfe1dc758c6140023a8", "field": {"Column": {"Expression": {"SourceRef": {"Entity": "FCT_RELIABILITY"}}, "Property": "YEAR"}}, "type": "Advanced"}, {"name": "945b3a000a9dc0aeea66", "field": {"Measure": {"Expression": {"SourceRef": {"Entity": "FCT_RELIABILITY"}}, "Property": "CA`
- **cardVisual** `60c7e3f0b4bead9c30cb` at x=1728 y=0 w=192 h=149
  - alt text: none
  - Data: [Selected Major Event Share] (measure on AmiEventStudy)
  - visual filters: `{"filters": [{"name": "5d95d5eeb9a7adbad560", "field": {"Measure": {"Expression": {"SourceRef": {"Entity": "AmiEventStudy"}}, "Property": "Selected Major Event Share"}}, "type": "Advanced"}]}`
- **cardVisual** `7f06e22e345306270702` at x=980 y=0 w=177 h=149
  - alt text: none
  - Data: [Selected Customers] (measure on AmiEventStudy)
  - visual filters: `{"filters": [{"name": "cf8cc8a8013d1e41eb83", "field": {"Measure": {"Expression": {"SourceRef": {"Entity": "AmiEventStudy"}}, "Property": "Selected Customers"}}, "type": "Advanced"}]}`
- **scatterChart** `826577f03738cae22210` at x=980 y=603 w=939 h=477
  - title/text: "More storm days, more outage minutes. 2025 sits where its weather predicts"
  - subtitle: "NOAA storm county-days in Dominion’s Virginia counties vs SAIDI ex MED, 2013 to 2025 | axis valueAxis: "Outage mins per customer"; categoryAxis: "Storm county-days (NOAA)""
  - alt text: none
  - Category: V_STORM_VS_SAIDI[YEAR] (column)
  - X: Sum of V_STORM_VS_SAIDI[STORM_COUNTY_DAYS]
  - Y: Sum of V_STORM_VS_SAIDI[SAIDI_EX_MED]
  - visual filters: `{"filters": [{"name": "a56a6036114982425308", "field": {"Column": {"Expression": {"SourceRef": {"Entity": "V_STORM_VS_SAIDI"}}, "Property": "YEAR"}}, "type": "Advanced"}, {"name": "3ae7e36803e72a867a03", "field": {"Aggregation": {"Expression": {"Column": {"Expression": {"SourceRef": {"Entity": "V_ST`
- **cardVisual** `85c7fe070bb08b249a19` at x=1157 y=0 w=159 h=149
  - alt text: none
  - Data: [Selected SAIDI] (measure on AmiEventStudy)
  - visual filters: `{"filters": [{"name": "7f14b70638d3b740ce17", "field": {"Measure": {"Expression": {"SourceRef": {"Entity": "AmiEventStudy"}}, "Property": "Selected SAIDI"}}, "type": "Advanced"}]}`
- **lineChart** `8cf55a203d9c93e66b58` at x=0 y=149 w=980 h=454
  - title/text: "Outages per customer up 6% since 2019, most of it after 2023"
  - subtitle: "SAIFI, excluding major event days. Dominion Energy Virginia, EIA-861 | axis valueAxis: "Outages per Customer per Year""
  - alt text: none
  - Category: FCT_RELIABILITY[YEAR] (column)
  - Y: [SAIFI ex MED] (measure on FCT_RELIABILITY)
  - visual filters: `{"filters": [{"name": "48d2522d08a906a341a0", "field": {"Column": {"Expression": {"SourceRef": {"Entity": "FCT_RELIABILITY"}}, "Property": "YEAR"}}, "type": "Advanced"}, {"name": "b769eb13e4dddd1eaede", "field": {"Measure": {"Expression": {"SourceRef": {"Entity": "FCT_RELIABILITY"}}, "Property": "SA`
- **slicer** `d841e406606cb6877656` at x=680 y=87 w=300 h=62
  - alt text: none
  - Values: Dashboard Year[Year] (column)
  - visual filters: `{"filters": [{"name": "7b320970637208035932", "field": {"Column": {"Expression": {"SourceRef": {"Entity": "Dashboard Year"}}, "Property": "Year"}}, "type": "Advanced"}]}`
- **textbox** `ed03849209beb1288bb0` at x=15 y=10 w=643 h=66
  - title/text: "Electricity Demand & Grid Planning"
  - alt text: none
- **cardVisual** `f34f7fc4d6b95e25b282` at x=1546 y=0 w=182 h=149
  - alt text: none
  - Data: [Selected SAIFI] (measure on AmiEventStudy)
  - visual filters: `{"filters": [{"name": "0088e3d33b7e530c592b", "field": {"Measure": {"Expression": {"SourceRef": {"Entity": "AmiEventStudy"}}, "Property": "Selected SAIFI"}}, "type": "Advanced"}]}`
- **cardVisual** `f37647b5550328452389` at x=1316 y=0 w=230 h=149
  - alt text: none
  - Data: [Selected CAIDI] (measure on AmiEventStudy)
  - visual filters: `{"filters": [{"name": "f1754b5fd732d0ce5cc0", "field": {"Measure": {"Expression": {"SourceRef": {"Entity": "AmiEventStudy"}}, "Property": "Selected CAIDI"}}, "type": "Advanced"}]}`
- **textbox** `f98b3d720c82504c0056` at x=15 y=75 w=643 h=66
  - title/text: "Customer outage trends, interruption drivers and weather exposure (EIA-861 & NOAA Storm Data)"
  - alt text: none

## Page `ca36f3cced18c2313453`: "Executive Dashboard-2" (1920x1080)

- **textbox** `0fb6bdf75ea43a197450` at x=15 y=10 w=643 h=66
  - title/text: "Reliability Performance & Drivers"
  - alt text: none
- **clusteredColumnChart** `10a79b0633cd9c8e9009` at x=0 y=539 w=951 h=541
  - title/text: "Winter peak now matches summer: higher in 2022, 2025 and 2026"
  - subtitle: "Highest hour in Dec to Feb vs Jun to Aug each year, PJM DOM zone, EIA-930. 2026 summer is complete, winter is Jan to Feb only | axis valueAxis: "Peak Demand, MW""
  - alt text: none
  - Category: DOM_LOAD_ANNUAL[YEAR] (column)
  - Y: [Winter peak MW] (measure on DOM_LOAD_ANNUAL)
  - Y: [Summer peak MW] (measure on DOM_LOAD_ANNUAL)
  - visual filters: `{"filters": [{"name": "f9ea788de356277992d6", "ordinal": 0, "field": {"Measure": {"Expression": {"SourceRef": {"Entity": "DOM_LOAD_ANNUAL"}}, "Property": "Summer peak MW"}}, "type": "Advanced"}, {"name": "c49ecb93430bfb2c2b29", "ordinal": 1, "field": {"Measure": {"Expression": {"SourceRef": {"Entity`
- **textbox** `158ceaf7ed6928cac954` at x=15 y=62 w=907 h=51
  - title/text: "Load growth, changing demand patterns and smart-meter adoption | EIA-861 & EIA-930"
  - alt text: none
- **cardVisual** `18d3b980d88222e2273d` at x=1279 y=541 w=333 h=100
  - alt text: none
  - Data: [Top 50 hours in 2025] (measure on DOM_TOP50_HOURS)
- **cardVisual** `19360d26904890819773` at x=1611 y=541 w=308 h=100
  - alt text: none
  - Data: [Peak growth 2019 to 2025] (measure on DOM_LOAD_ANNUAL)
- **clusteredBarChart** `1d92052046d0a3c7b466` at x=0 y=113 w=951 h=426
  - title/text: "The meters are installed. Almost nobody is on a rate that uses them"
  - subtitle: "Share of customers with a smart meter vs share on a time-varying rate, 2025. EIA-861 | axis valueAxis: "Share %""
  - alt text: none
  - Category: Programmes2025[utility] (column)
  - Y: [Smart meter share %] (measure on Programmes2025)
  - Y: [Time-varying rate %] (measure on Programmes2025)
  - visual filters: `{"filters": [{"name": "13f57dd78583a62c8dcc", "field": {"Column": {"Expression": {"SourceRef": {"Entity": "Programmes2025"}}, "Property": "utility"}}, "type": "Categorical", "filter": {"Version": 2, "From": [{"Name": "p", "Entity": "Programmes2025", "Type": 0}], "Where": [{"Condition": {"Not": {"Exp`
- **clusteredColumnChart** `71ceb4a586c3d3d3acb9` at x=952 y=641 w=968 h=439
  - title/text: "Load growth 2019 to 2025 by hour of day: night +41%, afternoon +27%"
  - subtitle: "Change in average demand for each hour of the day, PJM DOM zone, EIA-930 | axis valueAxis: "Growth %"; categoryAxis: "Hour of Day""
  - alt text: none
  - Category: DOM_LOAD_PROFILE[HOUR_NO] (column)
  - Y: Sum of DOM_LOAD_PROFILE[GROWTH_PCT]
- **cardVisual** `e12a05449550ed1cb6e0` at x=951 y=541 w=328 h=100
  - alt text: none
  - Data: [Floor growth 2019 to 2025] (measure on DOM_LOAD_ANNUAL)
- **lineChart** `f3f57290918057748a49` at x=951 y=0 w=969 h=541
  - title/text: "Commercial sales up 65% since 2013 on 8% more customers. That gap is data centres"
  - subtitle: "Retail sales and customer counts, 2013 = 100. Dominion Energy Virginia, EIA-861 | axis valueAxis: "Index, 2023 = 100""
  - alt text: none
  - Category: LoadGrowth[year] (column)
  - Y: Sum of LoadGrowth[commercial_sales_index]
  - Y: Sum of LoadGrowth[commercial_customers_index]
  - Y: Sum of LoadGrowth[residential_sales_index]
  - visual filters: `{"filters": [{"name": "ba3838d3204ac568a120", "field": {"Column": {"Expression": {"SourceRef": {"Entity": "LoadGrowth"}}, "Property": "year"}}, "type": "Advanced"}, {"name": "9d8fd9ced86501238332", "field": {"Aggregation": {"Expression": {"Column": {"Expression": {"SourceRef": {"Entity": "LoadGrowth`

## Visuals that aggregate a raw column (not a measure)

- Scorecards / `4815afead0c6a4a7ca4b` (cardVisual), Data: Sum of FCT_RELIABILITY[Customers Served]
- What Moved / `eb9e34101c7ddbafa3ba` (lineChart), Y: Sum of FCT_RELIABILITY[SAIFI_EX_MED]
- Weather / `0cdbc9919c3afef37960` (lineChart), Y: Sum of SAIDI_WEATHER_ADJUSTED[SAIDI_EX_MED]
- Weather / `0cdbc9919c3afef37960` (lineChart), Y: Sum of SAIDI_WEATHER_ADJUSTED[WEATHER_ADJUSTED_SAIDI]
- Weather / `cd3dca34756db97f5ed6` (scatterChart), X: Sum of V_STORM_VS_SAIDI[STORM_COUNTY_DAYS]
- Weather / `cd3dca34756db97f5ed6` (scatterChart), Y: Sum of V_STORM_VS_SAIDI[SAIDI_EX_MED]
- Growth / `3e0ddca78b79485a3fea` (lineChart), Y: Sum of LoadGrowth[commercial_sales_index]
- Growth / `3e0ddca78b79485a3fea` (lineChart), Y: Sum of LoadGrowth[commercial_customers_index]
- Growth / `3e0ddca78b79485a3fea` (lineChart), Y: Sum of LoadGrowth[residential_sales_index]
- Growth / `7b0e71f981e225998e87` (clusteredColumnChart), Y: Sum of DOM_LOAD_PROFILE[GROWTH_PCT]
- Executive Dashboard-1 / `1bc8e4107099744b0737` (lineChart), Y: Sum of SAIDI_WEATHER_ADJUSTED[SAIDI_EX_MED]
- Executive Dashboard-1 / `1bc8e4107099744b0737` (lineChart), Y: Sum of SAIDI_WEATHER_ADJUSTED[WEATHER_ADJUSTED_SAIDI]
- Executive Dashboard-1 / `826577f03738cae22210` (scatterChart), X: Sum of V_STORM_VS_SAIDI[STORM_COUNTY_DAYS]
- Executive Dashboard-1 / `826577f03738cae22210` (scatterChart), Y: Sum of V_STORM_VS_SAIDI[SAIDI_EX_MED]
- Executive Dashboard-2 / `71ceb4a586c3d3d3acb9` (clusteredColumnChart), Y: Sum of DOM_LOAD_PROFILE[GROWTH_PCT]
- Executive Dashboard-2 / `f3f57290918057748a49` (lineChart), Y: Sum of LoadGrowth[commercial_sales_index]
- Executive Dashboard-2 / `f3f57290918057748a49` (lineChart), Y: Sum of LoadGrowth[commercial_customers_index]
- Executive Dashboard-2 / `f3f57290918057748a49` (lineChart), Y: Sum of LoadGrowth[residential_sales_index]

Count: 18 projections in 10 visuals
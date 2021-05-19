# covid-19-genomes
Projects on topic of COVID-19 genomic sequencing - mostly DataViz

**Reference:**

International data on COVID-19 genomic sequencing data from the [GISAID project](https://www.gisaid.org), via: [outbreak.info](https://outbreak.info/location-reports?loc=AUS&selected=S%3AE484K&selected=B.1.1.7&selected=B.1.351&selected=B.1.617.2&selected=P.1&selected=B.1.427&selected=B.1.429&selected=B.1.526&selected=B.1.526.1&selected=B.1.526.2&selected=B.1.617&selected=B.1.617.1&selected=B.1.617.3&selected=P.2) and [nextstrain.org](https://nextstrain.org/ncov/global).

Following the visualisation style of [Trevor Bedford](https://twitter.com/trvrb/status/1392132870064381956?s=20).

**Summary**

The outbreak.info and nextstrain sites presents data on genomic sequencing by country, with limited interactivity.

In this project, the data from those sources is presented in an interactive data visualisation tool: [Power BI](https://powerbi.microsoft.com). This allows interactive filtering of the data in the table, for easier analysis.  The original data is quite noisy with many lineages presented together, over a long timescale. IMO the stacked area chart is not  ideal as it tends to obscure sharp rises in recent data (e.g. B.1.617.2 in Australia, April-May 2021).

The initial focus is on Australia and New Zealand. They are not often reported on, but have relatively high proportions of genomic sequences vs their COVID-19 cases.

Data for any country could be included - just download it from the outbreak.info page for the country (**Tracked lineages over time** section) in tsv format and refresh the PBIX file using Power BI Desktop. 

The data to translate country codes into names is read from [Wikipedia](https://en.wikipedia.org/wiki/List_of_ISO_3166_country_codes)

[Link to interactive DataViz](https://app.powerbi.com/view?r=eyJrIjoiNDgwNzc4ODMtNTk1Ny00MmE2LTgxOWEtYzY1MzZjYWFlMWU5IiwidCI6ImRjMWYwNGY1LWMxZTUtNDQyOS1hODEyLTU3OTNiZTQ1YmY5ZCIsImMiOjEwfQ%3D%3D)

[![Click to view and interact with the report](https://github.com/Mike-Honey/covid-19-genomes/raw/main/Coronavirus%20-%20Genomic%20epidemiology%20-%20AUS.png)](https://app.powerbi.com/view?r=eyJrIjoiNDgwNzc4ODMtNTk1Ny00MmE2LTgxOWEtYzY1MzZjYWFlMWU5IiwidCI6ImRjMWYwNGY1LWMxZTUtNDQyOS1hODEyLTU3OTNiZTQ1YmY5ZCIsImMiOjEwfQ%3D%3D)



THIS REPORT IS NOT HEALTH ADVICE - REFER TO YOUR LOCAL HEALTH AUTHORITY.


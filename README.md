# hrv_analysis

## Time range extractor

Make sure that `attyshrv_heartrate.tsv` and `adc_data.tsv` are in the subdir.

Then run:

```
python extract.py dd/mm/yyyy HH:MM:SS rawoutfile.tsv hroutfile.tsv
```
 
which extracts then 30min of data till the timestamps become discontinous or 30mins have elapsed.

## raw data and HR plot

```
plot_raw_hr.py rawfile hrfile
```

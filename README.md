# testdata
Testdata for the MInv FAT testing


## Refreshing the index.html files

To refresh the index.html files run the script ``generate_index_html.sh``:

    # for TDS1, TDS2, TDS3 and TDS32:

    for tds in TDS1 TDS2 TDS3 TDS32 TDS4 ; do
        for mission in `ls ${tds}` ; do
            for file_type in `ls ${tds}/${mission}` ; do
                ls ${tds}/${mission}/${file_type}/*index.zip | ./generate_index_html.sh > ${tds}/${mission}/${file_type}/index.html
            done
        done
    done


minv collection Envisat/ASA_IM__0P \
    -o http://data.eox.at/minv/meta/OADS1/Envisat/ASA_IM__0P/ \
    -o http://data.eox.at/minv/meta/OADS2/Envisat/ASA_IM__0P/ \
    -n http://data.eox.at/minv/meta/ngA1/Envisat/ASA_IM__0P/ \
    -n http://data.eox.at/minv/meta/ngA2/Envisat/ASA_IM__0P/

minv collection Envisat/ASA_IMS_1P \
    -o http://data.eox.at/minv/meta/OADS1/Envisat/ASA_IMS_1P/  \
    -o http://data.eox.at/minv/meta/OADS2/Envisat/ASA_IMS_1P/ \
    -n http://data.eox.at/minv/meta/ngA1/Envisat/ASA_IMS_1P/ \
    -n http://data.eox.at/minv/meta/ngA2/Envisat/ASA_IMS_1P/

minv collection SMOS/ECMWF_ \
    -o http://data.eox.at/minv/meta/OADS1/SMOS/AUX_Dynamic_Open/ \
    -o http://data.eox.at/minv/meta/OADS2/SMOS/AUX_Dynamic_Open/ \
    -n http://data.eox.at/minv/meta/ngA1/SMOS/AUX_Dynamic_Open/ \
    -n http://data.eox.at/minv/meta/ngA2/SMOS/AUX_Dynamic_Open/

for file_type in MIR_BWLD1C MIR_BWLF1C MIR_BWSD1C MIR_BWSF1C MIR_OSUDP2 MIR_SCLD1C MIR_SCLF1C MIR_SCSD1C MIR_SCSF1C MIR_SC_D1B MIR_SC_F1B MIR_SMUDP2 ; do
    minv collection SMOS/${file_type} \
        -n http://data.eox.at/minv/meta/ngA1/SMOS/${file_type}/ \
        -n http://data.eox.at/minv/meta/ngA2/SMOS/${file_type}/ \
        -o http://data.eox.at/minv/meta/OADS1/SMOS/SMOS_Open/ \
        -o http://data.eox.at/minv/meta/OADS2/SMOS/SMOS_Open/
done

minv config Envisat/ASA_IM__0P -i Envisat_ASA_IM__0P.conf
minv config Envisat/ASA_IMS_1P -i Envisat_ASA_IMS_1P.conf

minv config SMOS/ECMWF_ -i SMOS_ECMWF_.conf

# import collection configuration
for file_type in MIR_BWLD1C MIR_BWLF1C MIR_BWSD1C MIR_BWSF1C MIR_OSUDP2 MIR_SCLD1C MIR_SCLF1C MIR_SCSD1C MIR_SCSF1C MIR_SC_D1B MIR_SC_F1B MIR_SMUDP2 ; do 
    minv config SMOS/${file_type} -i SMOS_${file_type}.conf
done
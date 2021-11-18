#! bash

for db in $PCMRI_DATASETS/*; do
    for exam in $db/*; do
        for f in $exam/*; do
            enc=$(file $f)
            case $enc in 
                *ISO*)
                    echo "ISO > UTF8 $f"
                    cp $f $f.iso
                    iconv -f ISO-8859-8 -t UTF-8 $f.iso > $f
                    ;;
                *UTF*)
                    echo "UTF8 $f"
                    ;;
            esac
        done
    done
done
            


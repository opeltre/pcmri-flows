#! bash

for exam in $PCMRI_DATASETS/exams/*; do
    for f in $exam/*.txt; do
        echo $(basename $f) 
    done
done > filenames

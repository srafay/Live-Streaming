for ((i=1; i<=4; i++))
do
    printf "Recording stream #%d\n\n", "$i"
    python vlc.py "$i"
    printf "Finished stream #%d\n\n", "$i"
done

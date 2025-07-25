for i in $(seq 0 9); do \
  v=$(printf "%02X" "$i"); \
  raw_title=$(curl -s "https://random-word-api.herokuapp.com/word?number=3" | jq -r '. | join(" ")'); \
  title=$(echo "$raw_title" | sed 's/\b\(.\)/\u\1/g'); \
  echo "\n > Generating Chimerox #$v: $title"; \
  \
  desc=$(curl -s 'https://baconipsum.com/api/?type=meat-and-filler&paras=1' | jq -r '.[0]'); \
  \
  python3 chimerox.py --FHD --fps 30 --duration 90 \
    --meta "title:Chimerox #$v: $title" \
    --meta "description:$desc" \
    ~/chimerox_videos/chimerox_$v.mp4; \
done

for i in $(seq 0 9); do \
  v=$(printf "%02X" "$i"); \
  raw_title=$(curl -s "https://random-word-api.herokuapp.com/word?number=3" | jq -r '. | join(" ")'); \
  title=$(echo "$raw_title" | sed 's/\b\(.\)/\u\1/g'); \
  echo "\n > Generating Chimerox #$v: $title"; \
  \
  desc=$(curl -s 'https://baconipsum.com/api/?type=meat-and-filler&paras=1' | jq -r '.[0]'); \
  \
  python3 chimerox.py --FHD --fps 30 --duration 65 \
    --portrait \
    --meta "title:Chimerox #$v (Portrait): $title" \
    --meta "description:$desc" \
    ~/chimerox_videos/chimerox_SHORT$v.mp4; \
done


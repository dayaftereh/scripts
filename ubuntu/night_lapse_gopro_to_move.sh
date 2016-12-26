#!/bin/bash

INPUT="$1"

if [ -z "${INPUT}" ]; then
  echo "usage $0 INPUT_DIR [FPS]"
  exit 1
fi

if [ ! -d "$INPUT" ]; then
  echo "INPUT_DIR is not a directory!"
  exit 1
fi

FPS="$2"
if [ -z "${2}" ]; then
  FPS="2/1"
fi

OUTPUT="$INPUT/output"

if [ -d "$OUTPUT" ]; then
  rm -fr "$OUTPUT"
fi

mkdir "$OUTPUT"

i=1
for f in "$INPUT"/*; do
  if [ -f "$f" ]; then
    FILENAME=$(basename "$f")
    EXT="${FILENAME##*.}"


    COUNTER=$(printf %03d $i)
    OUTPUT_FILE="$OUTPUT/$COUNTER.$EXT"

    cp "$f" "$OUTPUT_FILE"
    i=$(($i+1))
  fi
done

OUTPUT_VIDEO_FILE="$INPUT/output.mp4"

if [ -f "$OUTPUT_VIDEO_FILE" ]; then
  rm -f "$OUTPUT_VIDEO_FILE"
fi

ffmpeg -framerate "$FPS" -i "$OUTPUT/%03d.JPG" -c:v libx264 -r 30 "$INPUT/output.mp4"

if [ -d "$OUTPUT" ]; then
  rm -fr "$OUTPUT"
fi

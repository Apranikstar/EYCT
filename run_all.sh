#!/bin/bash
source /cvmfs/sw.hsf.org/key4hep/setup.sh -r 2024-03-10
INDIR="/eos/experiment/fcc/ee/generation/DelphesEvents/winter2023/IDEA"
OUTDIR="./output/"
NCPUS=8

PROCESSES=(
  "Hlnuqq"
  "Hqqlnu"
  "enueqq"
  "eeqq"
  "munumuqq"
  "mumuqq"
  "taunutauqq"
  "tautauqq"
  "Htautau"
  "Hllnunu"
  "eenunu"
  "mumununu"
  "tautaununu"
  "l1l2nunu"
  "tautau"
  "Hgg"
  "Hbb"
  "qq"
)

for process in "${PROCESSES[@]}"
do
  echo "Running process: $process"
  python stage_all.py --indir "$INDIR" --outdir "$OUTDIR" --sample "wzp6_ee_${process}_ecm125" --ncpus "$NCPUS"
done


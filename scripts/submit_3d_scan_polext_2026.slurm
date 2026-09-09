#!/bin/bash
# 2026 lambda_pol extension scan (0-8, lambda_soc fixed at 0), UCR HPC.
# Re-run to fix a data-integrity gap the round-3 referee panel caught
# (2026-08-22): the manuscript/notebook cite specific 2026 lambda_pol=8
# numbers (best-T=0.37, per-seed std=0.6pp) that trace to NO file on disk --
# only the 2022 extension (scan_3d_2022_polext_pol{0..8}_soc0.npz) exists,
# and its own lambda_pol=8 point is T=0.69, not 0.37. This produces the
# actual 2026 data so the manuscript's circularity-check paragraph can cite
# real, traceable numbers. Same settings as the already-completed 2022
# extension run (submit_3d_scan.slurm's proven pattern, just year/prefix
# swapped): 9 lambda_pol points in [0,8], lambda_soc pinned to 0 via
# --n-lambda-soc 1 (linspace(0, max, 1) = [0.] regardless of max).

#SBATCH --job-name=isingcr-3d-scan-polext-2026
#SBATCH --account=c4139
#SBATCH --partition=shared
#SBATCH --qos=cpu
#SBATCH --array=0-8%9
#SBATCH --cpus-per-task=32
#SBATCH --time=01:00:00
#SBATCH --output=/scratch/global/tomas.rojas_s/isingcr/logs/3d_scan_polext_2026_%A_%a.out
#SBATCH --error=/scratch/global/tomas.rojas_s/isingcr/logs/3d_scan_polext_2026_%A_%a.err

set -euo pipefail

ISINGCR_PYTHON=/home/tomas.rojas_s/bin/miniforge3/envs/isingcr/bin/python
REPO_ROOT=/scratch/global/tomas.rojas_s/isingcr
cd "$REPO_ROOT"
mkdir -p data/processed

N_LAMBDA_POL=9
N_LAMBDA_SOC=1
N_TEMPERATURES=32
LAMBDA_MAX=8.0
OUTPUT_PREFIX=scan_3d_polext

echo "=== Pre-flight resource check (task ${SLURM_ARRAY_TASK_ID:-N/A} of array) ==="
"$ISINGCR_PYTHON" scripts/run_3d_scan.py --estimate \
    --n-lambda-pol "$N_LAMBDA_POL" --n-lambda-soc "$N_LAMBDA_SOC" \
    --n-temperatures "$N_TEMPERATURES" --lambda-max "$LAMBDA_MAX"

TASK_ID="${SLURM_ARRAY_TASK_ID:-0}"
LAMBDA_POL_IDX=$(( TASK_ID / N_LAMBDA_SOC ))
LAMBDA_SOC_IDX=$(( TASK_ID % N_LAMBDA_SOC ))
echo "Task $TASK_ID -> lambda_pol index $LAMBDA_POL_IDX, lambda_soc index $LAMBDA_SOC_IDX"

export OMP_NUM_THREADS=1
srun --exact -n 1 -c $SLURM_CPUS_PER_TASK "$ISINGCR_PYTHON" scripts/run_3d_scan.py \
    --n-lambda-pol "$N_LAMBDA_POL" --n-lambda-soc "$N_LAMBDA_SOC" \
    --n-temperatures "$N_TEMPERATURES" --lambda-max "$LAMBDA_MAX" \
    --output-prefix "$OUTPUT_PREFIX" \
    --lambda-pol-index "$LAMBDA_POL_IDX" --lambda-soc-index "$LAMBDA_SOC_IDX"

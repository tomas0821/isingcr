#!/bin/bash
# 2-task cluster submission for scripts/run_gam_field.py, UCR HPC.
# Task 0 = 2026, task 1 = 2022. Same cost profile as one point in the
# original run_3d_scan.py grid each (~21.7 min estimated, 30-32 min real).
# `shared` confirmed healthy 2026-08-21 (submit_prior_margin_field.slurm ran
# there cleanly) -- same account/QoS facts as that submission.

#SBATCH --job-name=isingcr-gam-field
#SBATCH --account=c4139
#SBATCH --partition=shared
#SBATCH --qos=cpu
#SBATCH --array=0-1%2
#SBATCH --cpus-per-task=32
#SBATCH --time=01:00:00
#SBATCH --output=/scratch/global/tomas.rojas_s/isingcr/logs/gam_field_%A_%a.out
#SBATCH --error=/scratch/global/tomas.rojas_s/isingcr/logs/gam_field_%A_%a.err

set -euo pipefail

ISINGCR_PYTHON=/home/tomas.rojas_s/bin/miniforge3/envs/isingcr/bin/python
REPO_ROOT=/scratch/global/tomas.rojas_s/isingcr
cd "$REPO_ROOT"
mkdir -p data/processed

TASK_ID="${SLURM_ARRAY_TASK_ID:-0}"
if [ "$TASK_ID" -eq 0 ]; then YEAR=2026; else YEAR=2022; fi
echo "Task $TASK_ID -> year $YEAR"

echo "=== Pre-flight resource check ==="
"$ISINGCR_PYTHON" scripts/run_gam_field.py --estimate

export OMP_NUM_THREADS=1
srun --exact -n 1 -c $SLURM_CPUS_PER_TASK "$ISINGCR_PYTHON" scripts/run_gam_field.py --year "$YEAR"

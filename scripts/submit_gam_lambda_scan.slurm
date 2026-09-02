#!/bin/bash
# lambda_soc scan for the GAM field (2026, N=488), UCR HPC. 9 lambda points
# (scripts/run_gam_lambda_scan.py LAMBDA_GRID), one per array task, each the
# same cost profile as one run_gam_field.py task (~21.7 min estimated,
# 30-32 min real on `shared`). Same account/QoS/partition facts as
# submit_gam_field.slurm, which ran cleanly there 2026-08-21.

#SBATCH --job-name=isingcr-gam-lambda
#SBATCH --account=c4139
#SBATCH --partition=shared
#SBATCH --qos=cpu
#SBATCH --array=0-8%9
#SBATCH --cpus-per-task=32
#SBATCH --time=01:00:00
#SBATCH --output=/scratch/global/tomas.rojas_s/isingcr/logs/gam_lambda_%A_%a.out
#SBATCH --error=/scratch/global/tomas.rojas_s/isingcr/logs/gam_lambda_%A_%a.err

set -euo pipefail

ISINGCR_PYTHON=/home/tomas.rojas_s/bin/miniforge3/envs/isingcr/bin/python
REPO_ROOT=/scratch/global/tomas.rojas_s/isingcr
cd "$REPO_ROOT"
mkdir -p data/processed logs

TASK_ID="${SLURM_ARRAY_TASK_ID:-0}"
echo "Task $TASK_ID -> lambda index $TASK_ID"

echo "=== Pre-flight resource check ==="
"$ISINGCR_PYTHON" scripts/run_gam_lambda_scan.py --estimate

export OMP_NUM_THREADS=1
srun --exact -n 1 -c $SLURM_CPUS_PER_TASK "$ISINGCR_PYTHON" scripts/run_gam_lambda_scan.py \
    --lambda-index "$TASK_ID"

#!/bin/bash
# Single-task cluster submission for scripts/run_prior_margin_field.py, UCR HPC.
# One field, one full 32-T pooled scan -- same cost as one point in the
# original run_3d_scan.py grid (~21.7 min estimated, 30-32 min real-world per
# this session's prior observations). `shared` confirmed healthy at submit
# time (2026-08-21): one node fully idle (0/64 allocated), so submitting
# there directly rather than mpi -- no need for mpi's 64-core floor for a
# single task. Same account/QoS facts as submit_3d_scan.slurm.

#SBATCH --job-name=isingcr-prior-margin
#SBATCH --account=c4139
#SBATCH --partition=shared
#SBATCH --qos=cpu
#SBATCH --cpus-per-task=32
#SBATCH --time=01:00:00
#SBATCH --output=/scratch/global/tomas.rojas_s/isingcr/logs/prior_margin_%j.out
#SBATCH --error=/scratch/global/tomas.rojas_s/isingcr/logs/prior_margin_%j.err

set -euo pipefail

ISINGCR_PYTHON=/home/tomas.rojas_s/bin/miniforge3/envs/isingcr/bin/python
REPO_ROOT=/scratch/global/tomas.rojas_s/isingcr
cd "$REPO_ROOT"
mkdir -p data/processed

echo "=== Pre-flight resource check ==="
"$ISINGCR_PYTHON" scripts/run_prior_margin_field.py --estimate

export OMP_NUM_THREADS=1
srun --exact -n 1 -c $SLURM_CPUS_PER_TASK "$ISINGCR_PYTHON" scripts/run_prior_margin_field.py

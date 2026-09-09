#!/bin/bash
# Single-task cluster submission for scripts/run_gam_susceptibility_scan.py, UCR HPC.
# Same cost profile as one point in the original run_3d_scan.py grid
# (~21.7 min estimated, 30-32 min real per this session's prior observations).

#SBATCH --job-name=isingcr-gam-chi-scan
#SBATCH --account=c4139
#SBATCH --partition=shared
#SBATCH --qos=cpu
#SBATCH --cpus-per-task=32
#SBATCH --time=01:00:00
#SBATCH --output=/scratch/global/tomas.rojas_s/isingcr/logs/gam_chi_scan_%j.out
#SBATCH --error=/scratch/global/tomas.rojas_s/isingcr/logs/gam_chi_scan_%j.err

set -euo pipefail

ISINGCR_PYTHON=/home/tomas.rojas_s/bin/miniforge3/envs/isingcr/bin/python
REPO_ROOT=/scratch/global/tomas.rojas_s/isingcr
cd "$REPO_ROOT"
mkdir -p data/processed

echo "=== Pre-flight resource check ==="
"$ISINGCR_PYTHON" scripts/run_gam_susceptibility_scan.py --estimate

export OMP_NUM_THREADS=1
srun --exact -n 1 -c $SLURM_CPUS_PER_TASK "$ISINGCR_PYTHON" scripts/run_gam_susceptibility_scan.py --year 2026

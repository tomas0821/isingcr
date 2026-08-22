#!/bin/bash
# Single-task cluster submission for scripts/run_gam_counterfactual_sweep.py, UCR HPC.
# Only 13 T points (not 32), and pooled_temperature_scan parallelizes over T,
# so min(32, 13)=13 cores is all that's actually used -- sized to match
# rather than requesting a full 32-core node and wasting 19 cores.

#SBATCH --job-name=isingcr-gam-counterfactual
#SBATCH --account=c4139
#SBATCH --partition=shared
#SBATCH --qos=cpu
#SBATCH --cpus-per-task=13
#SBATCH --time=00:45:00
#SBATCH --output=/scratch/global/tomas.rojas_s/isingcr/logs/gam_counterfactual_%j.out
#SBATCH --error=/scratch/global/tomas.rojas_s/isingcr/logs/gam_counterfactual_%j.err

set -euo pipefail

ISINGCR_PYTHON=/home/tomas.rojas_s/bin/miniforge3/envs/isingcr/bin/python
REPO_ROOT=/scratch/global/tomas.rojas_s/isingcr
cd "$REPO_ROOT"
mkdir -p data/processed

echo "=== Pre-flight resource check ==="
"$ISINGCR_PYTHON" scripts/run_gam_counterfactual_sweep.py --estimate

export OMP_NUM_THREADS=1
srun --exact -n 1 -c $SLURM_CPUS_PER_TASK "$ISINGCR_PYTHON" scripts/run_gam_counterfactual_sweep.py

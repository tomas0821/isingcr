#!/bin/bash
# Cluster submission template for scripts/run_mideplan_axis_screen.py, UCR HPC.
#
# 5 MIDEPLAN IDS axes x 2 years (2026, 2022) = 10 tasks, one full 32-T pooled
# scan each (lambda_pol=0, lambda_axis=1.5 fixed -- see the script's
# docstring), identical cost profile to one point in run_3d_scan.py's
# original 25-point grid: `python scripts/run_mideplan_axis_screen.py
# --estimate` (run 2026-08-21) gives ~21.7 min/task estimated, but
# submit_3d_scan.slurm's real completed tasks ran 30-32 min under actual
# node contention -- same --time=01:00:00 safety margin used there, reused
# here rather than re-deriving from scratch.
#
# Same account/partition/QoS facts already verified live for submit_3d_scan.slurm
# (this account's only QoS is `cpu`; `shared` partition mandatorily layers
# p-serial's 32-core/job cap on top; QoS `cpu` allows MaxJobsPerUser=10
# concurrently running) -- reused verbatim, not re-verified here since
# nothing about the account/partition changed between the two submissions.
#
# Task index -> (axis, year): axis_index = TASK_ID % 5, year = 2026 if
# TASK_ID < 5 else 2022. Axes in order: salud, participa, seguridad,
# educacion, economico (AXES in run_mideplan_axis_screen.py).
#
# UPDATE 2026-08-21: first submission (job 124350) went to `shared` per the
# header above, but `shared`/`debug`/`lab` were ALL found `drained` at
# submit time (0/0/128/128 idle, no reservation -- an external maintenance
# window, not a bug here; same failure mode as the mid-session `shared`
# drain documented in submit_3d_scan.slurm). `mpi` had 576 idle cores (9
# idle nodes) at the same moment, so switched partition=mpi and bumped
# --cpus-per-task 32->64 (mpi's p-parallel QoS enforces MinTRES=cpu=64, a
# floor not a ceiling -- same discovery as the earlier fs128/3d-scan
# incident). --array throttle dropped 10->9 to match 9 idle 64-core nodes.

#SBATCH --job-name=isingcr-mideplan-axis
#SBATCH --account=c4139
#SBATCH --partition=mpi
#SBATCH --qos=cpu
#SBATCH --array=0-9%9
#SBATCH --cpus-per-task=64
#SBATCH --time=01:00:00
#SBATCH --output=/scratch/global/tomas.rojas_s/isingcr/logs/mideplan_axis_%A_%a.out
#SBATCH --error=/scratch/global/tomas.rojas_s/isingcr/logs/mideplan_axis_%A_%a.err

set -euo pipefail

# Same proven deployment pattern as submit_3d_scan.slurm (full interpreter
# path, not bare python3/conda activate) -- see that file's comments for why.
ISINGCR_PYTHON=/home/tomas.rojas_s/bin/miniforge3/envs/isingcr/bin/python
REPO_ROOT=/scratch/global/tomas.rojas_s/isingcr
cd "$REPO_ROOT"
mkdir -p data/processed

N_AXES=5
TASK_ID="${SLURM_ARRAY_TASK_ID:-0}"
AXIS_IDX=$(( TASK_ID % N_AXES ))
if [ "$TASK_ID" -lt "$N_AXES" ]; then YEAR=2026; else YEAR=2022; fi
echo "Task $TASK_ID -> axis index $AXIS_IDX, year $YEAR"

echo "=== Pre-flight resource check (task $TASK_ID of array) ==="
"$ISINGCR_PYTHON" scripts/run_mideplan_axis_screen.py --estimate

export OMP_NUM_THREADS=1
srun --exact -n 1 -c $SLURM_CPUS_PER_TASK "$ISINGCR_PYTHON" scripts/run_mideplan_axis_screen.py \
    --year "$YEAR" --axis-index "$AXIS_IDX"

#!/bin/bash
# Cluster submission template for scripts/run_3d_scan.py's full grid, UCR HPC.
#
# Sizing below comes directly from `python scripts/run_3d_scan.py --estimate`
# run interactively before writing this file (2026-08-20), for the script's
# *default* grid (5 lambda_pol x 5 lambda_soc x 32 T x 16 seeds, distrito
# scale N=488, 20000+20000 sweeps -- same budget as run_distrito_ablation.py):
#
#   SLURM array tasks (one per lambda_pol/lambda_soc pair): 25
#   Cores per task (parallelizes over T, capped at the shared partition's
#     enforced 32-core ceiling -- see below): 32
#   Estimated wall time per task: ~21.7 min
#   Estimated total core-hours (all 25 tasks): ~289
#
# Queue limits independently VERIFIED live on the cluster 2026-08-20 (not
# just taken on faith) -- `sacctmgr show qos`, `scontrol show partition
# shared/mpi`, and a real fs128 test submission from a different project
# that hit these limits directly:
#   - This account (c4139) only has direct access to QoS `cpu`, not
#     `p-serial` -- requesting --qos=p-serial would be rejected outright.
#   - The `shared` partition itself mandatorily layers QoS `p-serial`
#     (MaxTRES=cpu=32,node=1) on TOP of whatever --qos a job requests --
#     that's where the 32-core/job ceiling actually comes from, confirmed by
#     watching a 64-core job land in QOSMaxCpuPerJobLimit on `shared` and
#     succeed once cut to <=32 cores or moved to `mpi` (whose own enforced
#     partition QoS, p-parallel, has no core cap).
#   - QoS `cpu` (this account's real QoS, set explicitly above) has
#     MaxJobsPerUser=10 (concurrently RUNNING) and MaxSubmitJobsPerUser=20
#     (submitted+pending+running), MaxWall=24h, and no MaxTRESPerUser (no
#     evidence of a cumulative per-user core cap) -- so up to 10 of our
#     32-core tasks can genuinely run at once, not just be pending.
#   --array=0-24%10 (SLURM's native array-concurrency throttle) matches the
#   real MaxJobsPerUser=10 ceiling directly, rather than the job-submission
#   ceiling of 20 (which would just leave the extra 10 tasks sitting
#   eligible-but-blocked by the QoS instead of by the array throttle --
#   same eventual outcome, %10 is just the honest number).
#
# With 10-way concurrency actually available: ceil(25/10) = 3 throttled
# waves x ~21.7 min ~= 65 min total, well inside the 24h wall-time cap --
# assuming the cluster currently has 10x32=320 idle cores free to grant us,
# which was NOT checked before this submission (only the QoS/partition
# rules were verified, not real-time cluster load).
#
# REALITY CHECK from the first real submission (2026-08-20): both of these
# assumptions were optimistic. (1) Concurrency: `shared` is only 2 nodes
# shared with everyone else on the cluster -- observed running concurrently
# at any moment ranged from 1 to 3 of our tasks, not 10, and `mpi` (896
# cores, 14 nodes) was checked live and found *fully saturated* (0 idle
# cores) at the same moment `shared` had idle capacity -- more raw capacity
# does not mean more availability. (2) Per-task time: real completed tasks
# took 30-32 min, not the estimated 21.7 min (the benchmark's 2.03ms/sweep
# assumed an uncontended core; under real node sharing it runs slower) --
# one task hit the original --time=00:35:00 limit and was killed mid-run
# (TIMEOUT) before finishing, silently leaving that grid point's output
# file as a stale leftover from an earlier run rather than absent, which is
# easy to mistake for a real result if you don't check job state/log
# timestamps. --time bumped to 01:00:00 below in response; a still-running
# task's time limit can't be extended after the fact (`scontrol update`
# denies it for RUNNING, only PENDING) so a failure already in flight when
# you notice this has to be individually resubmitted for its specific grid
# point via --lambda-pol-index/--lambda-soc-index, not just re-queued.
#
# If you change --n-lambda-pol/--n-lambda-soc/--n-temperatures below, RE-RUN
# the estimate first (`python scripts/run_3d_scan.py --estimate <same flags>`)
# and update --array/--cpus-per-task/--time to match -- this file does not
# recompute it for you at submit time, only documents the sizing that was
# actually checked.
#
# Each array task handles one (lambda_pol, lambda_soc) pair; task index maps
# to a grid position via N_LAMBDA_SOC below.

#SBATCH --job-name=isingcr-3d-scan
#SBATCH --account=c4139
#SBATCH --partition=shared
#SBATCH --qos=cpu
#SBATCH --array=0-24%10
#SBATCH --cpus-per-task=32
#SBATCH --time=01:00:00
#SBATCH --output=/scratch/global/tomas.rojas_s/isingcr/logs/3d_scan_%A_%a.out
#SBATCH --error=/scratch/global/tomas.rojas_s/isingcr/logs/3d_scan_%A_%a.err

set -euo pipefail

# Deployment-specific: this project's proven working pattern on THIS cluster
# (see setup_env.sbatch / subsample_check.sbatch, already run successfully
# from /scratch/global/tomas.rojas_s/isingcr/ prior to this scan) is a named
# conda env invoked by full interpreter path -- not bare `python3` (the
# login shell's default python3 has none of numpy/pandas/networkx/geopandas)
# and not `conda activate` (unreliable inside non-interactive batch shells).
# NOTE: #SBATCH --output/--error above must therefore be an absolute path
# that already exists BEFORE `sbatch` is invoked -- SLURM opens them at
# dispatch time, before this script body (and its own mkdir, below) runs;
# `mkdir -p /scratch/global/tomas.rojas_s/isingcr/logs` on the login node
# before submitting is required, not optional.
ISINGCR_PYTHON=/home/tomas.rojas_s/bin/miniforge3/envs/isingcr/bin/python
REPO_ROOT=/scratch/global/tomas.rojas_s/isingcr
cd "$REPO_ROOT"
mkdir -p data/processed

N_LAMBDA_POL=5
N_LAMBDA_SOC=5
N_TEMPERATURES=32
LAMBDA_MAX=2.0

# Pre-flight: print the task-count/core estimate for this exact grid so the
# log records what was actually requested, not just what this comment block
# claims -- catches a stale comment if the grid above is ever edited without
# re-running --estimate.
echo "=== Pre-flight resource check (task ${SLURM_ARRAY_TASK_ID:-N/A} of array) ==="
"$ISINGCR_PYTHON" scripts/run_3d_scan.py --estimate \
    --n-lambda-pol "$N_LAMBDA_POL" --n-lambda-soc "$N_LAMBDA_SOC" \
    --n-temperatures "$N_TEMPERATURES" --lambda-max "$LAMBDA_MAX"

# One array task = one (lambda_pol, lambda_soc) grid point, via
# --lambda-pol-index/--lambda-soc-index (each task runs just its own point,
# not the whole grid) -- output goes to
# data/processed/scan_3d_pol<i>_soc<j>.npz per task, so tasks never clobber
# each other; reassemble the full grid by loading all 25 files afterward.
TASK_ID="${SLURM_ARRAY_TASK_ID:-0}"
LAMBDA_POL_IDX=$(( TASK_ID / N_LAMBDA_SOC ))
LAMBDA_SOC_IDX=$(( TASK_ID % N_LAMBDA_SOC ))
echo "Task $TASK_ID -> lambda_pol index $LAMBDA_POL_IDX, lambda_soc index $LAMBDA_SOC_IDX"

# --exact -n 1 -c $SLURM_CPUS_PER_TASK matches subsample_check.sbatch's
# proven-working invocation exactly: one task, all its allocated CPUs, left
# for run_3d_scan.py's own ProcessPoolExecutor-based parallelism (over T) to
# use -- not srun-level/MPI task parallelism, which this codebase doesn't use.
export OMP_NUM_THREADS=1
srun --exact -n 1 -c $SLURM_CPUS_PER_TASK "$ISINGCR_PYTHON" scripts/run_3d_scan.py \
    --n-lambda-pol "$N_LAMBDA_POL" --n-lambda-soc "$N_LAMBDA_SOC" \
    --n-temperatures "$N_TEMPERATURES" --lambda-max "$LAMBDA_MAX" \
    --lambda-pol-index "$LAMBDA_POL_IDX" --lambda-soc-index "$LAMBDA_SOC_IDX"

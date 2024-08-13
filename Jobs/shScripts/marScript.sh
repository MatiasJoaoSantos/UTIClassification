#!/bin/bash
#SBATCH --job-name=uticlass  # Nome do trabalho
#SBATCH --output=/home_cerberus/disk2/haniel.botelho/uploads/Downloads/physionet.org/files/eicu-crd/2.0/Outputs/slurmOutputs/slurm-%j.out
#SBATCH --time=2:00:00              # Limite de tempo hrs:min:sec
#SBATCH -N 1                         # Número de nós
#SBATCH --nodelist=gorgona2          # Escolher o nó específico
#SBATCH --mail-type=ALL
#SBATCH --mail-user=aliciachavesdcc.ufmg.com

set -x # Todos os comandos também são exibidos

cd /home/all_home/matias.joao/

module list
module avail
module load python3.12.1

source .venv/bin/activate

jupyter nbconvert --to notebook --execute /home_cerberus/disk2/haniel.botelho/uploads/Downloads/physionet.org/files/eicu-crd/2.0/Classification.ipynb --output Classification1308.ipynb


hostname   # Exibir o nó alocado

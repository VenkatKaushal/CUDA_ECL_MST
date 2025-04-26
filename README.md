# CUDA_ECL_MST
Testing Various Optimizations in ECL_MST approach.


To run it in DGX:

1. Copy the files in the DGX node.
2. We need a Graph to test:
    - Look at https://snap.stanford.edu/data/
    - Download the graph in the format of "edgelist" (see the link above)
    - Copy the file to the DGX node
    - Rename it to "graph.txt"
    - Run the following command to convert it to .el format
    python3 
3. Run the following command to run the program:
    - module load cuda/11.7
    - nvcc -O3 -arch=sm_80 -o ecl_mst ecl_mst.cu
4. Create a slrum script:
    ```
    #!/bin/sh
    #SBATCH --job-name=test ## Job name
    #SBATCH --ntasks=1 ## Run on a single CPU
    #SBATCH --gres=gpu:a100_1g.5gb:1 ## example request for GPU (use ## for commenting in case, gpu:a100_3g.20gb:1 for 20gb GPU, mediumq)
    #SBATCH --time=00:03:00 ## Time limit hrs:min:sec
    #SBATCH --partition=shortq ## ( partition name )
    #SBATCH --qos=shortq ## ( QUEUE name )
    #SBATCH --mem=100M ##(16GB max for shortq users)
    ##The output of the scuessfully executed code will be saved
    ##in the file mentioned below. %u -> user, %x -> jon-name,
    ##%N -> the compute node (dgx1), %j-> job ID.
    #SBATCH --output=/scratch/%u/%x-%N-%j.out ##Output file
    ##The errors associated will be saved in the file below
    #SBATCH --error=/scratch/%u/%x-%N-%j.err ## Error file
    ##the following command ensures successful loading of modules
    . /etc/profile.d/modules.sh

    #Load modules if necessary
    module load cuda/11.7  # (if your DGX uses modules)

    #Print info
    nvidia-smi
    nvcc --version

    #Run your compiled program
    ./ecl_mst small.el
    ##ncu --set full ./ecl_mst small.el
    ```
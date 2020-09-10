import numpy as np

with open("ALPHA", "w") as alpha_file :
    with open("ELFCAR", "r") as elf_file :
        for line in elf_file :
            alpha_file.write(line)
            if len(line.split()) == 0 :
                break
        for line in elf_file :
            alpha_file.write(line)
            dimensions = np.array(line.split()).astype(int)
            break
        elf = list()
        for line in elf_file :
            elf += line.split()
            if len(elf) == np.prod(dimensions) :
                break
        elf = np.array(elf).astype(float)
        alpha = np.sqrt(1/elf-1)
        indices = np.arange(0, elf.shape[0], 10)
        for i in range(indices.shape[0]) :
            if i == indices.shape[0] - 1 :
                start = indices[i]
                stop = elf.shape[0]
            else :
                start = indices[i]
                stop = indices[i+1]
            line = " ".join([np.around(a, 5).astype(str) for a in alpha[start:stop]])
            alpha_file.write(line + "\n")

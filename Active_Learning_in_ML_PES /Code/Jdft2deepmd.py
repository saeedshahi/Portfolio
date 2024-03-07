PATH = 'C:/Users/Shahi/Desktop/Tanooj/'
number_of_atoms = 81
number_of_frames = 5001

def parse_outcar(infile_path):
    energy, lattice, positions, forces = [], [], [], []
    with open(infile_path, "r") as input_file:
        while True:
            line = input_file.readline()
            if not line:
                break  # End of file

            if 'direct lattice vectors' in line:  # lattice vectors
                lattice_vectors = [input_file.readline().strip().split()[0:3] for _ in range(3)]
                lattice.extend(sum([[float(x) for x in vec] for vec in lattice_vectors], []))

            if 'POSITION' in line:  # Skip the 'POSITION' line and the dashed line
                input_file.readline()  # Skip the dashed line after 'POSITION'
                for _ in range(number_of_atoms):
                    pos_line = input_file.readline().strip().split()
                    positions.extend([float(x) for x in pos_line[0:3]])
                    forces.extend([float(x) for x in pos_line[3:6]])

            if line.lower().startswith('  free  energy   toten'):
                energy.append(float(line.split()[-2]))

    return energy, lattice, positions, forces

def write_to_file(filepath, data, columns, fmt='{:.8f}'):
    with open(filepath, "w+") as file:
        for i in range(number_of_frames):
            line_data = data[i*columns:(i+1)*columns]
            file.write(' '.join(fmt.format(x) for x in line_data) + '\n')

infile_path = PATH + "stp.outcar"
energy, lattice, positions, forces = parse_outcar(infile_path)

write_to_file(PATH + "energy.raw", energy, 1)
write_to_file(PATH + "force.raw", forces, number_of_atoms*3, fmt='{:.6f}')
write_to_file(PATH + "coord.raw", positions, number_of_atoms*3, fmt='{:.5f}')
write_to_file(PATH + "box.raw", lattice, 9, fmt='{:.9f}')

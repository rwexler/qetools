from parsers import ParseDensityOfStates

ni2p_ni3h_dos = ParseDensityOfStates(
    path='tests/', indices=[0], weights=[1], spin=False)
ni2p_ni3h_dos.get_densities_of_states()

print(ni2p_ni3h_dos.__dict__)
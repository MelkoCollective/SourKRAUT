import os
import subprocess

def filterSpace(string):
    '''
    Simple filter function to remove "" terms from list.
    Used when reading lines from files.

    :param string: String element from list.
    :int string: str

    :returns: False is string is empty. True otherwise.
    :rtype: boolean
    '''
    if string == "":
        return False
    else:
        return True

def runSampling(numSamples,N,storeAmplitudes,showMakeOutput = False,showCCOutput = True):
    '''
    Makes and runs a c++ file for generating random samples
    of a quantum system. User also has the options of storing
    the amplitude coefficients and exact expectation values of
    observables.

    :param numSamples: Number of samples to generate.
    :type numSamples: int
    :param N: Number of qubits in the quantum system.
    :type N: int
    :param storeAmplitudes: Specify whether or not to store amplitudes.
    :type storeAmplitudes: bool
    :param showMakeOutput: Show output from running makefile.
                           Default is False.
    :type showMakeOutput: bool
    :param showCCOutput: Show output from running C++ ITensor file.
                         Default is True.
    :type showCCOutput: bool

    :returns: None
    '''

    if N > 20 and storeAmplitudes:
        print ("WARNING: Storing the amplitudes for a system size of 20 " +
               "or greater may require excessive memory. To avoid storing" +
               "the amplitudes, set storeAmplitudes to False.")

    __location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

    # Store the lines from the template c++ file
    template = open(os.path.join(__location__, "CppCode/Template/Heisenberg.cc"));
    templateLines = template.readlines()
    template.close()

    # Generate a new file with the required adjustments
    newFile = open(os.path.join(__location__, "CppCode/Heisenberg.cc"),"w");

    # This loop will rewrite the template lines to the new c++ file
    # while adjusting the lines as necessary based on the specified params
    for line in templateLines:
        los = list(filter(filterSpace,line.split(" ")))

        # Line adjustment for number of samples.
        if los[0] == "int" and los[1] == "numSamples":
            newFile.write("  int numSamples = {0};\n".format(numSamples))

        # Line adjustment for number of qubits
        elif los[0] == "const" and los[2] == "N":
            newFile.write("  const int N = {0};\n".format(N))

        # Line adjustment for storing amplitudes
        elif los[0] == "bool" and los[1] == "storeAmplitudes":
            amps = str(storeAmplitudes).lower()
            newFile.write("  bool storeAmplitudes = {0};\n".format(amps))

        # Line adjustment for obtaining amplitudes from MPS
        elif los[0] == "amplitude" and los[1] == "=":
            newFile.write(" " * 5 + "amplitude = R.real(spinIndices" +
                          "[{0}](bitset<N>(i)[0]+1),\n".format(N-1))
            for i in range(1,N-1):
                newFile.write(" " * 24 + "spinIndices" +
                              "[{0}](bitset<N>(i)[{1}]+1),\n".format(N-1-i,i))
            newFile.write(" " * 24 + "spinIndices" +
                          "[0](bitset<N>(i)[{0}]+1));\n".format(N-1))

        # Skip all subsequent amplitude coefficient lines
        elif "bitset<N>" in los[0]:
            pass

        # If no adjustment required then write the same line
        else:
            newFile.write(line)

    # Close our file and execute the new c++ script
    newFile.close()
    cppCodePath = os.path.join(__location__, "CppCode")
    p = subprocess.Popen(["chmod","a+x","Heisenberg"], cwd=cppCodePath)
    p.wait()
    if showMakeOutput:
        p = subprocess.Popen(["make"], cwd=cppCodePath)
        p.wait()
    else:
        FNULL = open(os.devnull,"w")
        p = subprocess.Popen(["make"], cwd=cppCodePath, stdout=FNULL,stderr=subprocess.STDOUT)
        p.wait()
    if showCCOutput:
        p = subprocess.Popen(["./Heisenberg"], cwd=cppCodePath)
        p.wait()
    else:
        FNULL = open(os.devnull,"w")
        p = subprocess.Popen(["./Heisenberg"], cwd=cppCodePath, stdout=FNULL,stderr=subprocess.STDOUT)
        p.wait()

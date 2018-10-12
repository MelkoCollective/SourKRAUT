from FrequencyCheck import countCheck
from OperatorCheck import operatorCheck

def RUN(check,numQubits,listofMs = None):
    '''
    Run operator and frequency checks on sample data produced from ITensor.

    :param check: Type of check to complete.
                  One of "Frequency" "S2S3" "H"
    :param numQubits: Number of qubits comprising the quantum system.
    :type numQubits: int
    :param listofMs: List of number of samples to try.
                     Does not need to be specified if check is Frequency.
    :type listofMs: listof int

    :returns: None
    '''
    if check == "Frequency":
        countCheck(numQubits)
    elif check == "S2S3":
        operatorCheck("S2S3",listofMs,numQubits)
    elif check == "H":
        operatorCheck("H",listofMs,numQubits)

RUN("H",20,range(100,50000,100))

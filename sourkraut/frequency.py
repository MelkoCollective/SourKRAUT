import numpy as np
import matplotlib.pyplot as plt
import itertools

def freqCheck(amplitudeFilename,samplesFilename,plotHistogram,showOutput):
    '''
    Compares expected and actual frequencies of each qubit configuration
    based on amplitude and sample files obtained from iTensor script.

    :param amplitudeFilename: Name of file containing amplitudes
    :type amplitudeFilename: str
    :param samplesFilename: Name of file containing samples
    :type samplesFilename: str
    :param plotHistogram: Specify whether or not to plot a histogram
                          comparing the expected and actual frequencies.
                          Recommended to be False if N > 9.
    :type plotHistogram: bool
    :param showOutput: Specify whether or not to print output.
    :type showOutput: bool

    :returns: Dictionary containing possible qubit configurations, list of
              observed frequencies and list of expected frequencies. All
              placed in the same order.
    :rtype: dict["configs"]
                ["actualFreq"]
                ["expectedFreq"]
    '''

    # Read and store amplitudes from amplitudes file
    amplitudes = []
    amplitudeFile = open(amplitudeFilename)
    lines = amplitudeFile.readlines()
    for line in lines:
        amplitudes.append(float(line.split(" ")[0]))
    amplitudeFile.close()

    # Read and store samples from sample file
    samples = []
    sampleFile = open(samplesFilename)
    lines = sampleFile.readlines()
    for line in lines:
        samples.append(line.replace(" ","").strip("\n"))
    sampleFile.close()

    # Store all possible qubit configurations in a list
    numOfQubits = len(samples[0])
    allCombos = list(itertools.product(["0","1"],repeat = numOfQubits))

    if numOfQubits > 9:
        print ("WARNING: Plotting a histogram for a system size of 10" +
               "or greater may greatly increase runtime. To avoid plotting" +
               "the histogram, set plotHistogram to False.")

    # Count the number of occurrences of each configuration from samples
    counter = {}
    for combo in allCombos:
        config = "".join(combo)
        counter[config] = 0
    for sample in samples:
        counter[sample] += 1

    # Print actual and expected number of occurrences of each configuration
    loopCounter = 0
    configs = []
    expectedFreq = []
    actualFreq = []
    for combo in allCombos:
        config = "".join(list(combo))
        expectedCount = int(len(samples) * amplitudes[loopCounter] ** 2)
        if showOutput:
            print("Number of occurrences of {0}: {1}".format(config,counter[config]))
            print("Number of expected occurrences of {0}: {1}".format(config,expectedCount))
            print("-------------------------------------------")
        loopCounter += 1
        configs.append(config)
        actualFreq.append(counter[config])
        expectedFreq.append(expectedCount)

    if plotHistogram:
        plt.bar(configs,actualFreq,label = "Actual")
        plt.bar(configs,expectedFreq,facecolor = "None",label = "Expected",edgecolor = "black",linewidth = 1.5)
        plt.legend(loc = "best")
        plt.xticks([])
        plt.xlabel("Various States")
        plt.ylabel("Counts")
        plt.title("Sampling from 1D Heisenberg Model for N = {0}".format(numOfQubits))
        plt.savefig("Histogram".format(numOfQubits),dpi = 200)

    results = {
        "configs":configs,
        "actualFreq":actualFreq,
        "expectedFreq":expectedFreq
    }

    return results

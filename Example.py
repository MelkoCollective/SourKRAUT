import sourkraut.frequency as sfreq
import sourkraut.operator as soper
import sourkraut.sampler as sampler

sampler.runSampling(20000,5,True)
sfreq.freqCheck("Amplitudes.txt","Samples.txt",True,True)
soper.operatorCheck("S2S3",range(100,20000,100),
                    "Amplitudes.txt","Samples.txt","Observables.txt")
soper.operatorCheck("H",range(100,20000,100),
                    "Amplitudes.txt","Samples.txt","Observables.txt")

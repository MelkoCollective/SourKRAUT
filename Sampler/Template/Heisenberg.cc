#include "itensor/all.h"
#include <cmath>
#include <iostream>
#include <fstream>
#include <bitset>
#include <numeric>
#include <iomanip>

using namespace itensor;
using namespace std;

int writeObservables (float S2S3,float H)
{
  // This function will be used to write the observables to a datafile
  ofstream myfile;
  myfile.open("Data/Observables.txt");

  std::string out_string1;
  std::stringstream ss1;
  ss1 << fixed;
  ss1 << std::setprecision(20) << S2S3;
  out_string1 = ss1.str();
  myfile << "S2S3: " + out_string1 + "\n";

  std::string out_string2;
  std::stringstream ss2;
  ss2 << fixed;
  ss2 << std::setprecision(20) << H;
  out_string2 = ss2.str();
  myfile << "H: " + out_string2 + "\n";

  myfile.close();
  return 0;
}

int writeAmplitudes (float loc[],int size)
{
  // This function will be used to write the amplitudes to a datafile
  ofstream myfile;
  myfile.open("Data/Amplitudes.txt");
  for (int i = 0; i < size; ++i) {
    float amp = loc[i];
    std::string out_string;
    std::stringstream ss;
    ss << fixed;
    ss << std::setprecision(10) << amp;
    out_string = ss.str();
      myfile << out_string + " 0.0000000000\n";
   }
  myfile.close();

  // Write a secondary file with all positive amplitude coefficients
  // in case one would like to use fidelity with QuCumber
  ofstream myfileP;
  myfileP.open("Data/AmplitudesP.txt");
  for (int i = 0; i < size; ++i) {
    float amp = abs(loc[i]);
    std::string out_string;
    std::stringstream ss;
    ss << fixed;
    ss << std::setprecision(10) << amp;
    out_string = ss.str();
      myfileP << out_string + " 0.0000000000\n";
   }
  myfileP.close();
  return 0;
}

int writeSamples (string los[],int size)
{
  // This function will be used to write the samples to a datafile
  ofstream myfile;
  myfile.open("Data/Samples.txt");
  for (int i = 0; i < size; ++i) {
    std::string sample = los[i];
    myfile << sample + "\n";
   }
  myfile.close();
  return 0;
}

int main()
{

  ////////////// PARAMETERS //////////////

  // Specify the number of samples to be taken
  int numSamples = 10000;

  // Specify number of sites
  const int N = 4;

  // Specify whether or not to store amplitude coefficients
  bool storeAmplitudes = true;

  ////////////// PARAMETERS //////////////

  // Define Hilbert space of N spin-half sites
  auto sites = SpinHalf(N);

  // Create 1d Heisenberg Hamiltonian
  auto ampo = AutoMPO(sites);
  for(int j = 1; j < N; ++j)
      {
      ampo += 0.5,"S+",j,"S-",j+1;
      ampo += 0.5,"S-",j,"S+",j+1;
      ampo +=   1,"Sz",j,"Sz",j+1;
      }
  auto H = MPO(ampo);

  // Set up random initial wavefunction
  auto psi = MPS(sites);

  // Specify number of sweeps of DMRG to perform
  // For 1D spin chains: Excellent results are normally obtained in as few
  // as 4 or 5 sweeps
  auto sweeps = Sweeps(5);

  // Specify max number of states kept each sweep
  // For 1D systems: bond dimensions in the hundreds are often sufficient
  // for high accuracy. First sweep should be 10 to 50 range.
  sweeps.maxm() = 50, 50, 100, 100, 200;

  // Run the DMRG algorithm
  // Optimizes the MPS based on the specified Hamiltonian
  // Returns the energy corresponding to the 1D Heisenberg Hamiltonian
  dmrg(psi,H,sweeps);

  // We can also try to calculate the energy exactly if the
  // computational cost is not too high. We should get the same value
  // as the dmrg value above.
  // <psi|H|psi>
  Real energy = overlap(psi,H,psi);

  // For the case of N = 3 psi consists of 3 tensors
  // ITensor r=2: ("S=1/2 1",2,Site|841) ("ul",2,Link|214)
  // ITensor r=3: ("S=1/2 2",2,Site|154) ("ul",2,Link|214) ("ul",2,Link|472)
  // ITensor r=2: ("S=1/2 3",2,Site|142) ("ul",2,Link|472)

  // tensorIndices stores the index set of each tensor
  // spinIndices stores the spin 1/2 index of each tensor
  // bondIndices stores the bond index of each tensor.
  // The ith element of bondIndices represents the bond between
  // tensors i and i+1.
  IndexSet tensorIndices[N] = {};
  Index spinIndices[N] = {};
  Index bondIndices[N] = {};

  for (int i = 0;i < N;i++) {
    tensorIndices[i] = psi.A(i+1).inds();
    if (i == N - 1) {
      spinIndices[i] = tensorIndices[i].index(1);
    } else {
      spinIndices[i] = tensorIndices[i].index(2);
    }
    if (i < N - 1) {
      bondIndices[i] = tensorIndices[i].index(1);
    }
  }

  if (storeAmplitudes == true) {
    // Contract each of the tensors in order to obtain a single
    // tensor containing the amplitude coefficients. At some
    // point this will too computationally intensive to complete.
    // Thus we will never a more clever method to determining
    // the fidelity.
    ITensor R = psi.A(1);
    for (int i = 2;i < N + 1;i++) {
      R *= psi.A(i);
    }

    // Normalize the amplitude coefficients
    auto nrm = norm(R);
    R /= nrm;

    // The following code will store all possible qubit configurations
    // These will be used to reference the amplitudes in the desired order
    int configs = pow(2,N);
    float amplitude = 0;
    float amplitudes[configs] = {};

    for(int i = 0;i < configs;i++) {
      amplitude = R.real(spinIndices[3](bitset<N>(i)[0]+1),
                         spinIndices[2](bitset<N>(i)[1]+1),
                         spinIndices[1](bitset<N>(i)[2]+1),
                         spinIndices[0](bitset<N>(i)[3]+1));
      amplitudes[i] = amplitude;
    }

    // Store the amplitude coefficients in a file
    // This will be used to measure fidelity
    writeAmplitudes(amplitudes,configs);
  }

  // Initiate random seed generator for measuring qubits
  srand(time(NULL));

  // Create an array to store the samples
  string los[numSamples] = {};

  // Contraction begins!

  // Compute Tr1 then Tr12 then Tr123...
  // Store them in an array for future reference
  ITensor contractions[N] = {};
  ITensor state = psi.A(1);

  for (int i = 0;i < N - 1;i++) {
    // At each iteration we prime the bond indices of the bra state
    // and contract to obtain partial trace Tr123...i
    if (i == 0) {
      state *= dag(prime(psi.A(i+1),bondIndices[i]));
    } else {
      state *= psi.A(i+1);
      state *= dag(prime(psi.A(i+1),bondIndices[i-1],bondIndices[i]));
    }
    contractions[i] = state;
  }

  for (int s = 0;s < numSamples;s++) {

    // Now we would like to obtain the reduced density matrices
    // which will contain the probabilities required for sampling
    int states[N] = {};
    float normFactor = 1;
    ITensor projectedStateKet = psi.A(N);
    ITensor projectedStateBra = dag(psi.A(N));

    for (int i = N-1;i >= 0;i--) {

      // Obtain reduced density matrix
      ITensor rho = psi.A(i+1);
      if (i > 0) {
        rho *= contractions[i-1];
      }

      if (i == N-1) {
        rho *= dag(prime(psi.A(i+1),bondIndices[i-1],spinIndices[i]));
      } else if (i == 0) {
        rho *= dag(prime(psi.A(i+1),bondIndices[i],spinIndices[i]));
        rho *= projectedStateKet;
        rho *= prime(projectedStateBra,bondIndices[i]);
      } else {
        rho *= dag(prime(psi.A(i+1),bondIndices[i-1],bondIndices[i],spinIndices[i]));
        rho *= projectedStateKet;
        rho *= prime(projectedStateBra,bondIndices[i]);
      }

      // Obtain rho indices so that probability can be referenced
      auto rhoIndices = rho.inds();
      auto rhoIndex1 = rhoIndices.index(1);
      auto rhoIndex2 = rhoIndices.index(2);
      float probQ0 = rho.real(rhoIndex1(1),rhoIndex2(1));
      probQ0 /= normFactor;

      // Measure the qubit and multiply normFactor by
      // probability of result for renormalization
      float randomNum = (rand() % 100 + 1)*0.01;
      if ((randomNum <= probQ0) || (probQ0 > 0.9999)) {
        states[i] = 0;
        normFactor *= probQ0;
      } else {
        states[i] = 1;
        normFactor *= 1 - probQ0;
      }

      // Project measurement onto sigma 4
      if (i > 0) {
        ITensor Spin(spinIndices[i]);
        if (states[i] == 0) {
          Spin.set(spinIndices[i](1),1);
          Spin.set(spinIndices[i](2),0);
        } else {
          Spin.set(spinIndices[i](1),0);
          Spin.set(spinIndices[i](2),1);
        }
        if (i < N-1) {
          projectedStateKet *= psi.A(i+1);
          projectedStateBra *= dag(psi.A(i+1));
        }
        projectedStateKet *= dag(Spin);
        projectedStateBra *= Spin;
      }

    }

    // Store sample as string.
    string sample = "";
    for (int i = N - 1;i >= 0;i--) {
        std::string Qstring;
        std::stringstream ss;
        ss << states[i];
        Qstring = ss.str();
        sample += Qstring;
        sample += " ";
    }
    reverse(sample.begin(), sample.end());
    los[s] = sample;

  }

  // Write samples to datafile
  writeSamples(los,numSamples);

  // Here we measure a two spin operator correlation function and compare
  // with the value obtained from sampling. We will use the second and
  // third spin operators.
  auto Sz2 = sites.op("Sz",2);
  auto Sz3 = sites.op("Sz",3);

  // Place the orthogonality center on site 2
  // This completes the contractions for us.
  psi.position(2);

  // Contract second ket tensor with operator
  ITensor C = psi.A(2);
  C *= Sz2;

  // Contract with second bra tensor while making sure to prime the site index
  // as well as the bond index that is common with the following tensor
  auto CI1 = commonIndex(psi.A(2),psi.A(3),Link);
  C *= dag(prime(prime(psi.A(2),Site),CI1));

  // Repeat similar process for third set of tensors
  C *= psi.A(3);
  C *= Sz3;
  auto CI2 = commonIndex(psi.A(3),psi.A(2),Link);
  C *= dag(prime(prime(psi.A(3),Site),CI2));

  // Result corresponding to <psi|S2S3|psi>
  auto result = C.real();
  println("Expectation value of S2S3 operator is ",result);

  // Write observable values to a datafile
  writeObservables(result,energy);
}

#! /usr/bin/env python
# -*- coding: iso-8859-15 -*-
"""Artificial neural networks for Orange.

  Orange module to add artificial neural networks as learning
  algorithms using calls to SNNS software.

  Version: 1.09 (working but some more testing and refinements
                 can improve it to version 1.10)

  SNNS randomness agrees with Orange behaviour on randomness:
   http://www.ailab.si/orange/doc/reference/random.htm
  
  In spite of the communicating media with SNNS being files, this code
  is supposed to be reentrant. Any way, as some of the temporal files
  are named by the module, but created by SNNS, there is a really
  extremely small chance of files becoming corrupted and
  breaking. Don't worry you would probably win the lotto and hang a
  windows program a billion times before this happens.

  TO DO:
  see marked XXX in code,
  error handling in system calls,
  error handling when SNNS fails,

Copyright (C) 2005-2006  Antonio Arauzo Azofra

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
"""

# From std python
import os, sys, string, re
import tempfile, math, random
from itertools import izip

# From orange
import orange, statc

# Should be set to the path where binaries of SNNS tools are
# located, if they are not in system path
pathSNNS = ""
# example:
#pathSNNS = "~/SNNSv4.2/tools/bin/i686-pc-linux-gnu/"

# If messages should be printed
verbose = False

def _argmax(array):
  """
  _argmax returns the position of the maximun value of an array
  """
  return max(izip(array,xrange(len(array))))[1]


class Transform:
  def __init__(self, table, alpha=0.1, beta=0.9):
    """
    Prepares transformation of data for neural network
      * discrete to N features in {alpha, beta}
      * continuous to [alpha, beta]

    Details of the transformation performed (transform):
      [(Continuous=True, slope, pos),(Continuous=False, no.values)]
      y = slope*x + pos

    Notes:

       Destination is not an orange.Example because we can not use
       more than one class feature in Orange

       Destination domain is formed by nnAntecedent values followed by
       nnTargets (following original order in each subgroup)
    
    """
    self.transform = []
    self.alpha = alpha
    self.beta = beta
    self.domain = table.domain   # Previous domain
    self.nnAntecedents = 0       # Transformed domain
    self.nnTargets = 0

    # Prepares transformation of data
    basicAttrStat = orange.DomainBasicAttrStat(table)

    for i in range( len(table.domain.variables) ):
      # Continuous
      if self.domain[i].varType == orange.VarTypes.Continuous:
        varRange = (basicAttrStat[i].max - basicAttrStat[i].min)
        if varRange == 0.0: 
          slope = 1.0 # Unique value
        else:
          slope = float(beta-alpha) / varRange
        pos = alpha - (slope * basicAttrStat[i].min)
        self.transform.append( (True, slope, pos) )

        if i != self.domain.variables.index(self.domain.classVar):
          self.nnAntecedents += 1
        else:
          self.nnTargets +=1

      # Discrete
      else:
        nValues = len( self.domain[i].values )
        self.transform.append( (False, nValues) )

        if i != self.domain.variables.index(self.domain.classVar):
          self.nnAntecedents += nValues
        else:
          self.nnTargets += nValues


  def apply(self, example):
    """
    Applies a defined trasformation over an example

    Returns: a list with the result
    """
    rtn = []

    # Antecedents
    for i in range( len(example) ):
      if i != self.domain.variables.index(self.domain.classVar):

        # Continuous
        if self.transform[i][0]:
          if example[i].value in ['?', '~', '.']:
            rtn.append(0.5)  # NULL values (uses average of [0,1]) XXX
          else:
            rtn.append( example[i]*self.transform[i][1] + self.transform[i][2] )

        # Discrete
        else:
          for j in range(self.transform[i][1]):
            if self.domain[i].values[j] == example[i]:
              rtn.append(self.beta)
            else:
              rtn.append(self.alpha)

    # Target (Class or goal attribute)
    i = self.domain.variables.index(self.domain.classVar)

    # Continuous
    if self.transform[i][0]:
      if example[i].value in ['?', '~', '.']:
        rtn.append(0.5)  # NULL values (uses average of [0,1]) XXX
      else:
        rtn.append( example[i]*self.transform[i][1] + self.transform[i][2] )

    # Discrete
    else:
      for j in range(self.transform[i][1]):
        if self.domain[i].values[j] == example[i]:
          rtn.append(self.beta)
        else:
          rtn.append(self.alpha)

    return rtn


  def applyInverseToTarget(self, target):
    """
    From a NN output get the class by: majority criterion, or
    denormalizing in continuous cases.

    Returns: orange.Value with the class
    """

    i = self.domain.variables.index(self.domain.classVar)

    if self.transform[i][0]: # continuous
      trTarget = (target[0] - self.transform[i][2]) / self.transform[i][1]
      rtn = orange.Value(self.domain.classVar, trTarget)

    else: # discrete
      rtn = orange.Value(self.domain.classVar, _argmax(target) )
      #XXX would not be nice if this worked in Orange:
      #    domain[i].values[_argmax(out)]

    return rtn


  def __str__(self):
    t = '<Transform:\n'

    for i in range( len(self.domain.variables) ):
      # Continuous
      t += self.domain[i].name + str( self.transform[i] ) + '\n'

    t += '>\n'
    return t


def savePatFile(table):
  """
  Given an orange example table create an SNNS pattern file.
  Transform data (using Transform):
   Normalize continuous data to [0,1].
   Discrete values to N inputs/outputs in {0,1}

  Caller is responsible for deleting pat file

  Returns: (patternFileName, transform)
  """

  # Prepares transformation of data
  transform = Transform(table, 0.1, 0.9)
  
  # Header
  text = "SNNS pattern definition file V1.4\n"
  text += "generated at Tue Jan 21 18:02:24 1997\n\n"
  text += "No. of patterns : " + str( len(table) ) + '\n'
  text += "No. of input units : " + str(transform.nnAntecedents) + '\n'
  text += "No. of output units : " + str(transform.nnTargets) + '\n'

  fd, patFileName = tempfile.mkstemp(suffix=".pat")
  patFile = os.fdopen(fd, "w")
  patFile.write(text)
  
  # Examples
  for example in table:
    text = ""
    trEx = transform.apply(example)
    for v in trEx:
      text += str(v) + ' '
    text += "\n"
    patFile.write(text)
      
  patFile.close()
  return (patFileName, transform)


def createNN(nInputs, hiddenLayers, nOutputs):
  """
  Creates a snns file with the topology of a multilayer
  completely connected aNN.

  Caller is responsible for deleting network file

  Returns: name of the file
  """
  
  # Prepare the name of the aNN
  hiddenName = ""
  for layer in hiddenLayers:
     hiddenName += str(layer) + "_"
  nnFileNamePrefix = "mlp" + str(nInputs) + "_" + hiddenName + str(nOutputs) + "-"
  nnFileName = tempfile.mktemp(prefix=nnFileNamePrefix, suffix=".net")

  # Build command for ff_bignet
  orden = pathSNNS + "ff_bignet" + " " + "-p " + str(nInputs) + " 1"
  for nNodes in hiddenLayers:
     orden = orden + " -p " + str(nNodes) + " 1"
  orden = orden + " -p " + str(nOutputs) + " 1"

  for j in range(len(hiddenLayers)+1):
     orden = orden + " -l " + str(j+1) + " + " + str(j+2) + " +"

  orden = orden + " " + nnFileName

  os.system(orden)
  return nnFileName


def trainNN(nnFileName, patternFileName, MSE, cycles, algorithm, learningParams):
  """
  Trains a neural network using batchman
  """

  # Open tmp file for the script
  try:
    fd, batchmanScriptFileName = tempfile.mkstemp()
    batchmanScriptFile = os.fdopen(fd, 'w')
  except IOError:
    print 'Error:  Couldn\'t create temp file.'
    sys.exit(0)

  # Create script batchman
  nu = 'loadNet("' + nnFileName + '")\n'
  nu += 'loadPattern("' + patternFileName + '")\n'
  nu += 'setInitFunc("Randomize_Weights", 1.0, -1.0)\n'
  nu += 'setLearnFunc("' + algorithm + '"' +\
        string.join(["," + p for p in learningParams], sep="") + ')\n'
  nu += 'setShuffle(TRUE)\n'
  nu += 'initNet()\n'
  nu += 'while CYCLES < ' + str(cycles) + ' and MSE > ' + str(MSE) + ' and SIGNAL == 0 do\n'
#  nu += 'if CYCLES mod 10 == 0 then\n'
#  nu += 'print ("cycles = ", CYCLES, "  SSE = ", SSE, " MSE = ",MSE) endif\n'
  nu += 'trainNet()\nendwhile\n'
  nu += 'if SIGNAL !=0 then print("Stopped due to signal reception: signal " + SIGNAL)\nendif'
  nu += '\nsaveNet("'+nnFileName+'")\n'

  batchmanScriptFile.write(nu)
  batchmanScriptFile.close()

  # Train the NN
  if verbose:
    orden = pathSNNS + "batchman    -f " + batchmanScriptFileName
  else:
    orden = pathSNNS + "batchman -q -f " + batchmanScriptFileName
  os.system(orden)

  # Remove tmp file
  os.remove(batchmanScriptFileName)


def trainAutoNN(nnFileName, trainFileName, testFileName, MSE, cycles, nRepeat, step, algorithm, learningParams):
  """

  Trains a neural network using batchman. Uses test data to evaluate
  the training state and select the best neural network.

  Bad accuracy (not used)
  """

  # Open tmp file for the script
  try:
    fd, batchmanScriptFileName = tempfile.mkstemp()
    batchmanScriptFile = os.fdopen(fd, 'w')
  except IOError:
    print 'Error:  Couldn\'t create temp file.'
    sys.exit(0)

  # Create script batchman
  nu = 'net = "' + nnFileName + '"\n'
  nu += 'loadNet(net)\n'
  nu += 'trainPat = "' + trainFileName + '"\n'
  nu += 'testPat = "' + testFileName + '"\n'
  nu += 'loadPattern(trainPat)\n'
  nu += 'loadPattern(testPat)\n'

  nu += 'setInitFunc("Randomize_Weights", 1.0, -1.0)\n'
  nu += 'setLearnFunc("' + algorithm + '"' +\
        string.join(["," + p for p in learningParams], sep="") + ')\n'
  nu += 'setShuffle(TRUE)\n'

  nu += 'mejor = 100000000   #Valor grande para representar +infinito\n'
  nu += 'for i:=1 to ' + str(nRepeat) + ' do\n'
  if verbose:
    nu += '  print(" --- ", i)\n'
  nu += '  initNet()\n'
  nu += '  while CYCLES < ' + str(cycles) + ' and MSE > ' + str(MSE) + ' and SIGNAL == 0 do\n'
  nu += '    setPattern(trainPat)\n'
  nu += '    for k:= 1 to ' + str(step) + ' do\n'
  nu += '       trainNet()\n'
  nu += '    endfor\n'
  nu += '    setPattern(testPat)\n'
  nu += '    testNet()\n'
  if verbose:
    nu += '    print("MSE =", MSE, "ciclos:", CYCLES)\n'
  nu += '    if MSE < mejor then\n'
  nu += '       mejor = MSE\n'
  nu += '       saveNet(net)\n'
  if verbose:
    nu += '       print(CYCLES, ": ", MSE, "(mejor MSE)")\n'
  nu += '    endif\n'
  nu += '  endwhile\n'
  nu += 'endfor\n'
  if verbose:
    nu += 'print("Mejor MSE(", net, ")= ", mejor)\n'
  nu += 'if SIGNAL !=0 then print("Stopped due to signal reception: signal " + SIGNAL)\nendif'

  batchmanScriptFile.write(nu)
  batchmanScriptFile.close()

  # Train the NN
  if verbose:
    orden = pathSNNS + "batchman    -f " + batchmanScriptFileName
  else:
    orden = pathSNNS + "batchman -q -f " + batchmanScriptFileName
    
  os.system(orden)

  # Remove tmp file
  os.remove(batchmanScriptFileName)
  #print "BATCHMAN:", batchmanScriptFileName

def guessTrainParameters(nnFileName, trainFileName, testFileName, MSE, cycles, nRepeat, step, algorithm, learningParams):
  """

  By a series of tests choose the number of cycles to train a neural
  network.

  """

  # Open tmp file for the script
  try:
    fd, batchmanScriptFileName = tempfile.mkstemp()
    batchmanScriptFile = os.fdopen(fd, 'w')
  except IOError:
    print 'Error:  Couldn\'t create temp file.'
    sys.exit(0)

  # Create script batchman
  nu  = 'net = "' + nnFileName + '"\n'
  nu += 'loadNet(net)\n'
  nu += 'trainPat = "' + trainFileName + '"\n'
  nu += 'testPat = "' + testFileName + '"\n'
  nu += 'loadPattern(trainPat)\n'
  nu += 'loadPattern(testPat)\n'

  nu += 'setInitFunc("Randomize_Weights", 1.0, -1.0)\n'
  nu += 'setLearnFunc("' + algorithm + '"' +\
        string.join(["," + p for p in learningParams], sep="") + ')\n'
  nu += 'setShuffle(TRUE)\n'

  nu += 'for i:=1 to ' + str(nRepeat) + ' do\n'
  nu += '  mejor = 100000000   #Valor grande para representar +infinito\n'
  nu += '  mejorCycles = 0\n'
  nu += '  print(" --- ", i)\n'
  nu += '  initNet()\n'
  nu += '  while CYCLES < ' + str(cycles) + ' and MSE > ' + str(MSE) + ' and SIGNAL == 0 do\n'
  nu += '    setPattern(trainPat)\n'
  nu += '    for k:= 1 to ' + str(step) + ' do\n'
  nu += '       trainNet()\n'
  nu += '    endfor\n'
  nu += '    setPattern(testPat)\n'
  nu += '    testNet()\n'
  nu += '    print("MSE =", MSE, "ciclos:", CYCLES)\n'
  nu += '    if MSE < mejor then\n'
  nu += '       mejor = MSE\n'
  nu += '       mejorCycles = CYCLES\n'
  nu += '       print(CYCLES, ": ", MSE, "(mejor MSE)")\n'
  nu += '    endif\n'
  nu += '  endwhile\n'
  nu += '  print("SetCycles=", mejorCycles)\n'
  nu += 'endfor\n'
  nu += 'print("Mejor MSE(", net, ")= ", mejor)\n'
  nu += 'if SIGNAL !=0 then print("Stopped due to signal reception: signal " + SIGNAL)\nendif'

  batchmanScriptFile.write(nu)
  batchmanScriptFile.close()

  # Train the NN
  if verbose:
    orden = pathSNNS + "batchman    -f " + batchmanScriptFileName
  else:
    orden = pathSNNS + "batchman -q -f " + batchmanScriptFileName
    
  inout = os.popen2(orden)

  cycles = []
  l = inout[1].readline()
  while l:
    if l[0:10] == "SetCycles=":
      cycles.append( int(l[10:]) )
    #print l,
    l = inout[1].readline()
    
  if verbose:
    print "cycles=", cycles

  # Remove tmp file
  os.remove(batchmanScriptFileName)

  return int( statc.mean(cycles) )
  

def extractWeights(nnFN):
  """
  Extract weights and bias from a neural network trained file
  """
  f = open(nnFN, 'r')
  aLine = f.readline()
  if aLine.find("SNNS network") == -1:
      raise Exception(nnFN + " is not an SNNS network")

  # Extract bias
  while not aLine.find("unit definition section") != -1:
      aLine = f.readline()

  dre = re.compile("\d")
  while not dre.search(aLine):
      aLine = f.readline()

  bias = []
  while dre.search(aLine):
      tokens = re.split('\|', aLine)
      b = float( tokens[4] )
      bias.append(b)
      aLine = f.readline()

  # Extract weights
  while not aLine.find("connection definition section") != -1:
      aLine = f.readline()

  dre = re.compile("\d")
  while not dre.search(aLine):
      aLine = f.readline()

  weightVectors = []
  while dre.search(aLine):
      cols = re.split('\|', aLine)
      tokens = cols[2].strip()
      while tokens[-1] == ',':
        tokens += f.readline().strip()

      tokens = re.split('^[^:]*:|,[^:]*:', tokens)
      weights = [float(w) for w in tokens if w != '']
      weightVectors.append(weights)
      aLine = f.readline()

  f.close()
  return (weightVectors, bias)



# --------------Learner classes (orange integration)------------------

def SNNSLearner(examples=None, **kwds):
    learner = SNNSLearner_Class(*(), **kwds)
    if examples:
        return learner(examples)
    else:
        return learner


class SNNSLearner_Class:
  """
  Artificial Neural Network(ANN) learner class that uses SNNS to
  create and train the ANN.
  """

  def __init__(self, name='SNNS neural network', hiddenLayers=None,
               MSE=0, cycles=200, auto=False, nRepeat=3, step=50,
               percentTrain=0.90,
               algorithm=None, learningParams=None):
        """
        Initializes a new neural network learner, defining the
        structure of the networks and training parameters.

        By now the structure is a multilayered perceptron

         name = learner name

         hiddenLayers = a list with the number of nodes of each hidden layer
         MSE = stop training if mse is smaller than this value
         cycles = stop training after this number of cycles
         
         auto = Whether trainNN (False) or trainAutoNN (True) is used
         nRepeat = if auto, the number of times the net is trained
         step = if auto, the number of cycles between one test and the next one
         percentTrain = if auto, the proportion of patterns used for training
        
         algorithm = name of training algorithm as identified in SNNS
         learningParams = list of strings with the parameters as in SNNS 
        """

        self.name         = name
        self.hiddenLayers = hiddenLayers
        self.MSE          = MSE
        self.cycles       = cycles

        self.auto         = auto 
        self.nRepeat      = nRepeat
        self.step         = step
        self.percentTrain = percentTrain

        if algorithm:
          self.algorithm = algorithm
        else:
          self.algorithm = "Std_Backpropagation"

        if learningParams:
          self.learningParams = learningParams
        else:
          self.learningParams = []


  def __call__(self, t, weight=None):
      patFileName, transform = savePatFile(t)

      # If input has no feature with values return a Majority classifier
      if transform.nnAntecedents < 1:
        return orange.MajorityLearner(t)

      if not self.hiddenLayers:
        self.hiddenLayers = [ (transform.nnAntecedents + transform.nnTargets)/2 ]

      nnFN = createNN(transform.nnAntecedents,
                      self.hiddenLayers,
                      transform.nnTargets)

      if self.auto:
        selection = orange.MakeRandomIndices2(t, self.percentTrain)
        trnPatFileName, transform = savePatFile( t.select(selection, 0) )
        testPatFileName, ignore = savePatFile( t.select(selection, 1) )
        cycles = guessTrainParameters(nnFN, trnPatFileName, testPatFileName,
                                  self.MSE, self.cycles, self.nRepeat, self.step,
                                  self.algorithm, self.learningParams)
      else:
        cycles = self.cycles

      trainNN(nnFN, patFileName, self.MSE, cycles,
              self.algorithm, self.learningParams)

      # Extract info from nnFile
      weights, bias = extractWeights(nnFN)

      nn = {'in': transform.nnAntecedents,
            'hidden': self.hiddenLayers,
            'out': transform.nnTargets,
            'weights': weights,
            'bias': bias}

      os.remove(patFileName)
      os.remove(nnFN)
      if self.auto:
        os.remove(trnPatFileName)
        os.remove(testPatFileName)
        
      # This self.domain seems needed by orgnFSS.FilteredClassifier
      # orange bug or misfeature?? XXX report
      # domain = t.domain
      # Note: -this is used to know which atts are being used by the learner
      # -Could be used to check that every example agrees on domain (maybe
      # not efficient)

      return SNNSClassifier(nn=nn, transform=transform, domain = t.domain)




class SNNSClassifier:
    def __init__(self, transform, name=None, **kwds):
        self.__dict__ = kwds
        if not name:
          self.name="snns"
        self.transform = transform

    def __call__(self, exampleOfAnySize, resultType = orange.GetValue):
        # Need to perform feature filtering because
        # IMHO this should be the duty of orngFSS.FilteredClassifier.__call__
        # to achieve transparency of FS in learning methods XXX report

        # Workaround to avoid the problem that appears in examples
        # with less features:
        workaround_domain = orange.Domain([a.name for a in self.transform.domain],
                                          exampleOfAnySize.domain)
        example = orange.Example(workaround_domain, exampleOfAnySize)

        exTr = self.transform.apply(example)  
        output = self.simulateNN(exTr[:self.transform.nnAntecedents])
        v = self.transform.applyInverseToTarget(output)

        if resultType == orange.GetValue:
          return v
        elif resultType == orange.GetProbabilities:
          return output
        else:
          return (v,output)

    def __str__(self):
      t = '<orangeSNNS:\n'

      t += str(self.transform) + '\n'

      t += str(self.nn)
      t += '>'
      return t

    def simulateNN(self, inputs):
      """
      Evaluates feed-fordward neural network with Logistic
      activation function
      """

      layersSize = self.nn['hidden'] + [ self.nn['out'] ]
      wRow = 0
      bPos = len(inputs)
      act = inputs

      for n in layersSize:
        act = self.layer(act, self.nn['weights'][wRow:wRow+n],
                         self.nn['bias'][bPos:bPos+n])
        wRow += n
        bPos += n
      print act,
      return act

    def layer(self, inputs, weights, bias):
      """
      Evaluates a layer (used by simulateNN)
      """
      n = len(weights)
      out = [None] * n
      for i in range(n):
        sum = 0
        for j in range( len(inputs) ):
          sum += inputs[j] * weights[i][j]
        sum += bias[i]
        out[i] = 1 / (1 + math.exp(-sum) )
      return out



# --- main - test ----------------------------------------------
# (Unsorted tests used for development)

if __name__ == "__main__":
  import orngTest, orngStat
  import gc, os, re, fileinput

  f = sys.argv[1]
  data = orange.ExampleTable(f)

  snns0 = SNNSLearner(name="snns", hiddenLayers=[4,2], cycles=100)
  regresor=snns0(data)

  sse = 0.0
  print "Results (test)"
  for e in data:
      print e, "->", regresor(e)

##  snns1 = SNNSLearner(name="snns0.2", auto=True, cycles=100, step=10, learningParams=["0.2"])
##  snns2 = SNNSLearner(cycles=2000, learningParams=["0.2"])
##  snns3 = SNNSLearner(cycles=2500, learningParams=["0.2"])

##  learners = [snns1]#, snns1,snns2,snns3]

##  # compute accuracies on data
##  results = orngTest.crossValidation(learners, data, folds=5)

##  # Print results
##  if data.domain.classVar.varType == orange.VarTypes.Continuous:
##    print "\nLearner       MSE      SE     #Atts SE"
##    for i in range(len(learners)):
##      mse, se = complete.MSE_se(results, reportSE=1)[i]
##      print "%-15s %6.2f %5.3f" % (learners[i].name, mse, se) 

##  else:
##    print "\nLearner       Accuracy SE     #Atts SE"
##    for i in range(len(learners)):
##      ca, se = orngStat.CA_se(results)[i]
##      ca, se = ca * 100, se * 100
##      print "%-15s %6.2f %5.3f" % (learners[i].name, ca, se) 




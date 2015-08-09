# Word Segmentation using Unidirectional RNNLM: Tuur, Kata, Stalin
import argparse
import subprocess
import sys
import os
import shutil



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Given a text file, and a prob-threshold trains a bi-directional RNNLM, and segments the text according to those places where the threshold is reached.')
    parser.add_argument('text', metavar='text', type=str,
                   help='The input text')
    parser.add_argument('-threshold', metavar='-threshold', type=float,default = 0.1,
                   help='The prob threshold (default=0.1)')
    parser.add_argument('-rnnlm', metavar='rnnlm', type=str, default='./rnnlm',
                   help='file path to the rnnlm program (default=./rnnlm)')
    parser.add_argument('-output', metavar='output', type=str, default='segmented.txt',
                   help='segmented output file (default: segmented.txt)')
    parser.add_argument('-clean', metavar='clean', type=int, default=1,
                   help='Clean tmp folder, containing intermediate steps: 1 (default), OR 0)')
    parser.add_argument('-fast', metavar='fast', type=int, default=1,
                   help='Runs each RNNLM only for one iteration, is faster, but the LM is less accurate.(default=1)')

    args = parser.parse_args()  
    
    if not(os.path.isfile(args.rnnlm)):
        sys.stderr.write('ERROR: Please provide a valid rnnlm path (option: -rnnlm rnnlmFilePath)\n')
        exit()
        
    tmpFolder = args.output + '-tmp/'
    
    if not(os.path.exists(tmpFolder)):
        os.makedirs(tmpFolder)
    else:
        shutil.rmtree(tmpFolder)
        os.makedirs(tmpFolder)
        
     
    # Split text in training and development texts, and reverse the text, for the RNNLM training
    sys.stderr.write('(1) Preparing for RNNLM training...\n')
    
    trainFile = open(tmpFolder + 'train.tmp', 'w')
    devFile = open(tmpFolder + 'dev.tmp','w')
    trainFileR = open(tmpFolder + 'train-r.tmp', 'w')
    devFileR = open(tmpFolder + 'dev-r.tmp','w')
    textFile = open(tmpFolder + 'text.tmp','w')
    textFileR = open(tmpFolder + 'text-r.tmp','w')    
    
    with open(args.text) as f:
        lines = f.readlines()
        
        # Split text into train and dev
        lineNr = 0
        for line in lines:
            words = line.rstrip().split()
            if lineNr%5 == 0:
                devFile.write(' '.join(words)+'\n')
                devFileR.write(' '.join(reversed(words))+'\n')                
            else:
                trainFile.write(' '.join(words)+'\n')
                trainFileR.write(' '.join(reversed(words))+'\n')
            lineNr+=1
            textFile.write(' '.join(words)+'\n')
            textFileR.write(' '.join(reversed(words))+'\n')
        trainFile.close()
        devFile.close()
        textFile.close()
        trainFileR.close()
        devFileR.close() 
        textFileR.close()


    sys.stderr.write('(2) Training & Running RNNLM -> ...\n')
    FNULL = open(os.devnull, 'w')
    # Training RNNLM
    command = [args.rnnlm,'-hidden','20', '-train', tmpFolder + 'train.tmp', '-valid',tmpFolder + 'dev.tmp','-rnnlm',tmpFolder + 'model.tmp']
    if args.fast:
        command += ['-one-iter']
        sys.stderr.write('fast-training=1\n')
    subprocess.call(command, shell=False, stdout=FNULL) 
    
    # Running RNNLM           
    with open(tmpFolder + 'out.tmp','w') as output:
        subprocess.call([args.rnnlm,'-rnnlm',tmpFolder + 'model.tmp','-test', tmpFolder + 'text.tmp','-debug','2'], shell=False, stdout=output)

        
    sys.stderr.write("(2') Training & Running RNNLM <- ...\n")
    # Training RNNLM-R
    command = [args.rnnlm, '-hidden','20', '-train', tmpFolder + 'train-r.tmp', '-valid',tmpFolder + 'dev-r.tmp','-rnnlm',tmpFolder + 'model-r.tmp']
    if args.fast:
        command +=['-one-iter']
        sys.stderr.write('fast-training=1\n')
    subprocess.call(command, shell=False, stdout=FNULL)

    # Running RNNLM-R
    with open(tmpFolder + 'out-r.tmp','w') as outputR:
        subprocess.call([args.rnnlm,'-rnnlm',tmpFolder + 'model-r.tmp','-test', tmpFolder + 'text-r.tmp','-debug','2'], shell=False, stdout=outputR)
    
    FNULL.close()

    # Reading RNNLM output
    outProbs = []
    with open(tmpFolder + 'out.tmp') as output:
        read = False
        probs = []
        for line in output:
            if read:
                try:
                    count, prob, word = line.split()
                    prob = float(prob)
                    if word == '</s>':
                        outProbs += [probs]
                        probs = []
                    else:
                        probs += [(word, prob)]
                except:
                        sys.stderr.write(':'+line[:-1]+'\n') 
            if line=='----------------------------------\n': # last line of training output
                    sys.stderr.write('(3) Reading RNNLM output ->...\n')
                    read=True
                      
    # Reading RNNLMR output-r
    outProbsR = []
    with open(tmpFolder + 'out-r.tmp') as output:
        read = False
        probs = []
        for line in output:
            if read:
                try:
                    count, prob, word = line.split()
                    prob = float(prob)
                    if word == '</s>':
                        outProbsR += [list(reversed(probs))]
                        probs = []
                    else:
                        probs += [(word, prob)]
                except:
                        sys.stderr.write(':'+line[:-1]+'\n') 
            if line=='----------------------------------\n': # last line of training output
                    sys.stderr.write('(3) Reading RNNLM output <-...\n')
                    read=True
           
    print len(outProbs)
    print len(outProbsR) 
    print '--'   

    sys.stderr.write('(4) Segmenting Text...\n')
    with open(args.output,'w') as segmented:
        for i in range(0,len(outProbs)): # for each line
            firstword = True
            for j in range(0,len(outProbs[i])): # for each word
                word1, prob1 = outProbs[i][j]
                word2, prob2 = outProbsR[i][j]
                
                if (prob1*prob2) > args.threshold or firstword:
                    segmented.write(word1)
                    firstword = False
                else:
                    segmented.write(' '+word1)
            segmented.write('\n')

    if args.clean:
        shutil.rmtree(tmpFolder)
    exit()

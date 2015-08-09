# Iterates the uni, and bi-directional rnnlm segmenter, Tuur, Kata & Stalin
import argparse
import subprocess
import sys
import os
import shutil

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Given a text file, iterates uni-directional or bi-directional RNNLM-word-segmentation.')
    parser.add_argument('text', metavar='text', type=str,
                   help='The input text')
    parser.add_argument('-threshold', metavar='-threshold', type=float,default = .2,
                   help='The prob threshold (default=0.2)')
    parser.add_argument('-rnnlm', metavar='rnnlm', type=str, default='./rnnlm',
                   help='file path to the rnnlm program (default=./rnnlm)')
    parser.add_argument('-it', metavar='it', type=int, default=10,
                   help='Number of iterations (default=10)')
    parser.add_argument('-method', metavar='method', type=str, default='bi',
                   help='Segmenting using uni-directional probabilities, or bi-directional probabilities; bi (default) or uni)')
    parser.add_argument('-fast', metavar='fast', type=int, default=1,
                   help='Segments much faster, but uses only one training iteration for the RNNLMs (default=1)')
    parser.add_argument('-output', metavar='output', type=str, default='iterations/',
                   help='Output folder to which the segmentations should be written (1 file / iteration), default = "iterations/"')

    args = parser.parse_args()  

    
    if args.method == 'uni':
        segmenter = 'uni-rnnlm-segment.py'
    elif args.method == 'bi':
        segmenter = 'bi-rnnlm-segment.py'
    else:
        sys.stderr.write('ERROR: No valid segmentation method given (-method bi OR -method uni)!')
        exit()

    if not(os.path.exists(args.output)):
        os.makedirs(args.output)
    else:
        shutil.rmtree(args.output)
        os.makedirs(args.output)
        
    sys.stderr.write('=== RNNLM Segmentation:\n')    
    sys.stderr.write('--- ITERATION 1:\n')
    subprocess.call(['python2.7',segmenter,args.text,'-threshold',str(args.threshold), '-output',args.output+'/seg-1.txt', '-fast', str(args.fast)])

    for i in range(1,args.it):
        sys.stderr.write('--- ITERATION '+str(i+1)+':\n')
        inp = args.output+'/seg-'+str(i)+'.txt'
        outp = args.output+'/seg-'+str(i+1)+'.txt'
        subprocess.call(['python2.7',segmenter,inp,'-threshold',str(args.threshold),'-output', outp, '-fast', str(args.fast)])

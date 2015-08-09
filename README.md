# segmental

RNNLM Segmenter
---------------
Given a fully separated space (character-) separated text, finds segments by concatenating units
for which the probability is higher than a given threshold.
Probability on a unit is calculated using recurrent neural network based language models.
There are two versions:
* **uni-directional**, using only left-to-right probability
* **bi-directional**, using the sum of both left-to-right, and right-to-left probability.
The segmenter runs in iterations. In each iteration a new language model is built, based on the segmentation from the previous iteration.


Code
----
###Requirements
* [rnnlm](http://www.fit.vutbr.cz/~imikolov/rnnlm/) (tested on version 0.3e)
* [python](https://www.python.org/download/releases/2.7/) (version 2.7)

###Example

`python2.7 iterate-rnnlm-segment.py -rnnlm ./rnnlm -it 100 -method bi -fast 1 -threshold 0.5 -output iterations/ data/1M.en.chars.txt` 

### Help 
```
Given a text file, iterates uni-directional or bi-directional RNNLM-word-segmentation.

positional arguments:
  text                  The input text

optional arguments:
  -h, --help            show this help message and exit
  -threshold -threshold
                        The prob threshold (default=0.5)
  -rnnlm rnnlm          file path to the rnnlm program (default=./rnnlm)
  -it it                Number of iterations (default=10)
  -method method        Segmenting using uni-directional probabilities, or bi-
                        directional probabilities; bi (default) or uni
  -fast fast            Segments much faster, but uses only one training
                        iteration for the RNNLMs (default=1)
  -output output        Output folder to which the segmentations should be
                        written (1 file / iteration), default = "iterations/"```



# 1-tk1-torch-zener-learner
Simple neural net to classify zener cards
## Zener cards?
In the 1930s psychologist Karl Zener designed a set of five cards to be used in experiments conducted with paraphyschologist Joseph Rhine.

![Zener Cards Image - Circle, Cross, Wavy Lines, Square, Star](https://github.com/mlennox/1-tk1-torch-zener-learner/blob/master/data/Zener_cards_color.svg.png)
Image by Mikhail Ryazanov (talk) 01:30, 1 April 2014 (UTC) (File:Cartas Zener.svg + File:Zenerkarten c.jpg) [GFDL (http://www.gnu.org/copyleft/fdl.html) or CC-BY-SA-3.0 (http://creativecommons.org/licenses/by-sa/3.0/), via Wikimedia Commons]

The experimenter would choose a card from a pack of 25, which contained five sets of the five cards shown in the image above - Circle, Cross, Wavy Lines, Square and Star. If the experimental subject guessed correctly more than 20% of the time then it could be possible that they are endowed with supernatural abilities. Or not, the experiments never conclusivel proved ESP.

I hope the parallel with machine learning classification is obvious and in this repo I will attempt to train a Torch7 based neural net (non-convolutional) running on a Jetson TK1 to properly classify Zener Cards.

## Test data
We will attempt to generate a large data set starting only with the symbols taken from the image above. 
To achieve this I will use Python to distort, scale and transpose the initial data.
It is likely I will add more starting data to the examples, but for now these will suffice as it is a simple neural net the risk of over-fitting is somewhat lower.

## The symbols

[https://github.com/mlennox/1-tk1-torch-zener-learner/blob/master/data/zener-images/circle.png]

[https://github.com/mlennox/1-tk1-torch-zener-learner/blob/master/data/zener-images/cross.png]

[https://github.com/mlennox/1-tk1-torch-zener-learner/blob/master/data/zener-images/wavy.png]

[https://github.com/mlennox/1-tk1-torch-zener-learner/blob/master/data/zener-images/square.png]

[https://github.com/mlennox/1-tk1-torch-zener-learner/blob/master/data/zener-images/star.png]

## Data expansion
After a cursory search I couldn't find any tools that would help me generate extra data from an existing data set. The first part of this project will require the creation of some Python scripts to fold, spindle and mutilate the starting data set.

## Data format
I will dicover what the data format should be as I progress in building out this network. I'll update this section as I know more.

